from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
from pathlib import Path


async def get_users_user_id(db: Session, user_id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.user_id == user_id))

    users_one = query.first()

    users_one = (
        (users_one.to_dict() if hasattr(users_one, "to_dict") else vars(users_one))
        if users_one
        else users_one
    )

    res = {
        "users_one": users_one,
    }
    return res


async def get_users(db: Session):

    query = db.query(models.Users)

    users_all = query.all()
    users_all = (
        [new_data.to_dict() for new_data in users_all] if users_all else users_all
    )
    res = {
        "users_all": users_all,
    }
    return res


async def put_users_user_id(db: Session, user_id: int, username: str, email: str):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.user_id == user_id))
    users_edited_record = query.first()

    if users_edited_record:
        for key, value in {
            "email": email,
            "user_id": user_id,
            "username": username,
        }.items():
            setattr(users_edited_record, key, value)

        db.commit()
        db.refresh(users_edited_record)

        users_edited_record = (
            users_edited_record.to_dict()
            if hasattr(users_edited_record, "to_dict")
            else vars(users_edited_record)
        )
    res = {
        "users_edited_record": users_edited_record,
    }
    return res


async def delete_users_user_id(db: Session, user_id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.user_id == user_id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict()
    else:
        users_deleted = record_to_delete
    res = {
        "users_deleted": users_deleted,
    }
    return res


async def get_user_roles(db: Session):

    query = db.query(models.UserRoles)

    user_roles_all = query.all()
    user_roles_all = (
        [new_data.to_dict() for new_data in user_roles_all]
        if user_roles_all
        else user_roles_all
    )
    res = {
        "user_roles_all": user_roles_all,
    }
    return res


async def get_user_roles_user_id(db: Session, user_id: int):

    query = db.query(models.UserRoles)
    query = query.filter(and_(models.UserRoles.user_id == user_id))

    user_roles_one = query.first()

    user_roles_one = (
        (
            user_roles_one.to_dict()
            if hasattr(user_roles_one, "to_dict")
            else vars(user_roles_one)
        )
        if user_roles_one
        else user_roles_one
    )

    res = {
        "user_roles_one": user_roles_one,
    }
    return res


async def post_user_roles(db: Session, raw_data: schemas.PostUserRoles):
    user_id: int = raw_data.user_id
    role_id: int = raw_data.role_id
    assigned_at: datetime.datetime = raw_data.assigned_at

    record_to_be_added = {
        "role_id": role_id,
        "user_id": user_id,
        "assigned_at": assigned_at,
    }
    new_user_roles = models.UserRoles(**record_to_be_added)
    db.add(new_user_roles)
    db.commit()
    db.refresh(new_user_roles)
    user_roles_inserted_record = new_user_roles.to_dict()

    res = {
        "user_roles_inserted_record": user_roles_inserted_record,
    }
    return res


async def put_user_roles_user_id(
    db: Session, user_id: int, role_id: int, assigned_at: str
):

    query = db.query(models.UserRoles)
    query = query.filter(and_(models.UserRoles.user_id == user_id))
    user_roles_edited_record = query.first()

    if user_roles_edited_record:
        for key, value in {
            "role_id": role_id,
            "user_id": user_id,
            "assigned_at": assigned_at,
        }.items():
            setattr(user_roles_edited_record, key, value)

        db.commit()
        db.refresh(user_roles_edited_record)

        user_roles_edited_record = (
            user_roles_edited_record.to_dict()
            if hasattr(user_roles_edited_record, "to_dict")
            else vars(user_roles_edited_record)
        )
    res = {
        "user_roles_edited_record": user_roles_edited_record,
    }
    return res


async def delete_user_roles_user_id(db: Session, user_id: int):

    query = db.query(models.UserRoles)
    query = query.filter(and_(models.UserRoles.user_id == user_id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        user_roles_deleted = record_to_delete.to_dict()
    else:
        user_roles_deleted = record_to_delete
    res = {
        "user_roles_deleted": user_roles_deleted,
    }
    return res


async def get_roles(db: Session):

    query = db.query(models.Roles)

    roles_all = query.all()
    roles_all = (
        [new_data.to_dict() for new_data in roles_all] if roles_all else roles_all
    )
    res = {
        "roles_all": roles_all,
    }
    return res


async def get_roles_role_id(db: Session, role_id: int):

    query = db.query(models.Roles)
    query = query.filter(and_(models.Roles.role_id == role_id))

    roles_one = query.first()

    roles_one = (
        (roles_one.to_dict() if hasattr(roles_one, "to_dict") else vars(roles_one))
        if roles_one
        else roles_one
    )

    res = {
        "roles_one": roles_one,
    }
    return res


async def put_roles_role_id(db: Session, role_id: int, role_name: str):

    query = db.query(models.Roles)
    query = query.filter(and_(models.Roles.role_id == role_id))
    roles_edited_record = query.first()

    if roles_edited_record:
        for key, value in {"role_id": role_id, "role_name": role_name}.items():
            setattr(roles_edited_record, key, value)

        db.commit()
        db.refresh(roles_edited_record)

        roles_edited_record = (
            roles_edited_record.to_dict()
            if hasattr(roles_edited_record, "to_dict")
            else vars(roles_edited_record)
        )
    res = {
        "roles_edited_record": roles_edited_record,
    }
    return res


async def delete_roles_role_id(db: Session, role_id: int):

    query = db.query(models.Roles)
    query = query.filter(and_(models.Roles.role_id == role_id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        roles_deleted = record_to_delete.to_dict()
    else:
        roles_deleted = record_to_delete
    res = {
        "roles_deleted": roles_deleted,
    }
    return res


async def post_users(db: Session, raw_data: schemas.PostUsers):
    user_id: int = raw_data.user_id
    username: str = raw_data.username
    email: str = raw_data.email

    record_to_be_added = {"email": email, "user_id": user_id, "username": username}
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    users_inserted_record = new_users.to_dict()

    # while loop
    while user_id == user_id:
        pass

    res = {
        "users_inserted_record": users_inserted_record,
    }
    return res


async def post_roles(db: Session, raw_data: schemas.PostRoles):
    role_id: int = raw_data.role_id
    role_name: str = raw_data.role_name

    record_to_be_added = {"role_id": role_id, "role_name": role_name}
    new_roles = models.Roles(**record_to_be_added)
    db.add(new_roles)
    db.commit()
    db.refresh(new_roles)
    roles_inserted_record = new_roles.to_dict()

    for role_1 in range(role_id, 1):
        pass

    res = {
        "roles_inserted_record": roles_inserted_record,
    }
    return res
