import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.comment import Comment, CommentVote
from app.models.user import User
from app.models.prediction import Prediction
from app.schemas.comment import CommentCreate, CommentResponse, VoteRequest

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/predictions/{prediction_id}/comments",
    response_model=list[CommentResponse],
    summary="Get Comments for a Prediction",
    description="Retrieve all community comments for a specific prediction case.",
)
async def get_comments(
    prediction_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pred_res = await db.execute(select(Prediction).where(Prediction.id == prediction_id))
    if not pred_res.scalar_one_or_none():
        raise HTTPException(
            status_code=404,
            detail="Prediction post not found"
        )

    query = (
        select(Comment, User.username, User.role)
        .join(User, Comment.user_id == User.id)
        .where(Comment.prediction_id == prediction_id)
        .order_by(Comment.created_at.asc())
    )
    result = await db.execute(query)
    rows = result.all()

    votes_res = await db.execute(
        select(CommentVote)
        .where(CommentVote.user_id == current_user.id)
    )
    user_votes = {v.comment_id: v.vote_type for v in votes_res.scalars().all()}

    response_data = []
    for comment, username, role in rows:
        response_data.append(
            CommentResponse(
                id=comment.id,
                prediction_id=comment.prediction_id,
                user_id=comment.user_id,
                content=comment.content,
                upvotes=comment.upvotes,
                downvotes=comment.downvotes,
                created_at=comment.created_at,
                username=username,
                user_role=role,
                user_vote=user_votes.get(comment.id),
            )
        )

    return response_data

@router.post(
    "/predictions/{prediction_id}/comments",
    response_model=CommentResponse,
    status_code=201,
    summary="Create a Comment",
    description="Post a new comment on a prediction case.",
)
async def create_comment(
    prediction_id: uuid.UUID,
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pred_res = await db.execute(select(Prediction).where(Prediction.id == prediction_id))
    pred = pred_res.scalar_one_or_none()
    if not pred:
        raise HTTPException(
            status_code=404,
            detail="Prediction post not found"
        )

    comment = Comment(
        id=uuid.uuid4(),
        prediction_id=prediction_id,
        user_id=current_user.id,
        content=comment_in.content,
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    return CommentResponse(
        id=comment.id,
        prediction_id=comment.prediction_id,
        user_id=comment.user_id,
        content=comment.content,
        upvotes=comment.upvotes,
        downvotes=comment.downvotes,
        created_at=comment.created_at,
        username=current_user.username,
        user_role=current_user.role,
        user_vote=None,
    )

@router.post(
    "/comments/{comment_id}/vote",
    response_model=CommentResponse,
    summary="Vote on a Comment",
    description="Upvote or downvote a comment. Voting again with the same type toggles/cancels it.",
)
async def vote_comment(
    comment_id: uuid.UUID,
    vote_in: VoteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vote_type = vote_in.vote_type.lower()
    if vote_type not in ("upvote", "downvote"):
        raise HTTPException(
            status_code=400,
            detail="Invalid vote type. Use upvote or downvote."
        )

    comment_res = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = comment_res.scalar_one_or_none()
    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    existing_vote_res = await db.execute(
        select(CommentVote)
        .where(and_(CommentVote.comment_id == comment_id, CommentVote.user_id == current_user.id))
    )
    existing_vote = existing_vote_res.scalar_one_or_none()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            if vote_type == "upvote":
                comment.upvotes = max(0, comment.upvotes - 1)
            else:
                comment.downvotes = max(0, comment.downvotes - 1)
            await db.delete(existing_vote)
            user_vote = None
        else:
            if vote_type == "upvote":
                comment.upvotes += 1
                comment.downvotes = max(0, comment.downvotes - 1)
            else:
                comment.downvotes += 1
                comment.upvotes = max(0, comment.upvotes - 1)
            existing_vote.vote_type = vote_type
            db.add(existing_vote)
            user_vote = vote_type
    else:
        new_vote = CommentVote(
            comment_id=comment_id,
            user_id=current_user.id,
            vote_type=vote_type
        )
        if vote_type == "upvote":
            comment.upvotes += 1
        else:
            comment.downvotes += 1
        db.add(new_vote)
        user_vote = vote_type

    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    author_res = await db.execute(
        select(User.username, User.role).where(User.id == comment.user_id)
    )
    author = author_res.all()
    author_username = author[0][0] if author else "Unknown"
    author_role = author[0][1] if author else "FARMER"

    return CommentResponse(
        id=comment.id,
        prediction_id=comment.prediction_id,
        user_id=comment.user_id,
        content=comment.content,
        upvotes=comment.upvotes,
        downvotes=comment.downvotes,
        created_at=comment.created_at,
        username=author_username,
        user_role=author_role,
        user_vote=user_vote,
    )
