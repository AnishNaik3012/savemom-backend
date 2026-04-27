

import uuid
from datetime import datetime, time, timedelta
from typing import List, Optional

from matplotlib import category
from numpy import require
from sqlalchemy import JSON, TIMESTAMP, Enum, ForeignKey, String, Integer, DateTime, Boolean, Time, func, Text, null, text, UniqueConstraint, TypeDecorator, Uuid
# from sqlalchemy.dialects.postgresql import UUID, ARRAY

class UUID(TypeDecorator):
    """Platform-independent UUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(32), storing as string without dashes.
    """
    impl = Uuid
    cache_ok = True

class ARRAY(TypeDecorator):
    """Platform-independent ARRAY type using JSON for SQLite."""
    impl = JSON
    cache_ok = True
    def __init__(self, item_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from db.db import Base
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
from sqlalchemy import Float
# from sqlalchemy.dialects.postgresql import JSONB
JSONB = JSON # Fallback for SQLite


# class User(Base):
#     __tablename__ = "User"

#     id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)


# class Appointment(Base):
#     __tablename__ = "Appointment"
        
#     id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,default=uuid.uuid4)		

# class Role(Base):
#     __tablename__ = "roles"

#     id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

# class EntityType(Base):
#     __tablename__ = "entityType"
#     id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)


class User(Base):
    __tablename__ = "User"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phoneVerified: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    country_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    password: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    emailVerified: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    gender: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    dob: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    roleId: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("roles.id", use_alter=True, name="fk_user_role"), nullable=True)
    userType: Mapped[str] = mapped_column(String, default="User")
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 
    adline1: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    adline2: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    pincode: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    active : Mapped[bool] = mapped_column(Boolean,server_default=text('TRUE'))
    isUnsubscribed : Mapped[bool] = mapped_column(Boolean, server_default=text('FALSE'), default=False)

    lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lng: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    subscribedPlan: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("userSubscription.id"), nullable=True)

    entity : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("entity.id"), nullable=True)

    userEntity: Mapped[Optional["Entity"]] = relationship("Entity", back_populates="users", foreign_keys=[entity])

    Qualification : Mapped[Optional[str]] = mapped_column(String, nullable=True) #Qualification
    Occupation : Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    pregnancyState : Mapped[Optional[str]] = mapped_column(String, nullable=True)

    specialty : Mapped[Optional[str]] = mapped_column(String, nullable=True)

    role: Mapped[Optional["Role"]] = relationship("Role", back_populates="users", foreign_keys=[roleId])

    familyID : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("Family.id"), nullable=True)

    notificationChannels: Mapped[List[str]] = mapped_column(ARRAY(String), default=["email", "sms", "push","whatsapp","voice"], nullable=True)

    notificationsSubscribed: Mapped[List[str]] = mapped_column(ARRAY(String), default=["anc", "lab_test", "vaccine","weekly_tips"], nullable=True)


    isDeleted: Mapped[bool] = mapped_column(Boolean, nullable=True)
    phoneAtDelete: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    createdRoles: Mapped[List["Role"]] = relationship("Role", back_populates="createdByUser", foreign_keys="Role.createdBy")
    
    createdById: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_user_created_by"), nullable=True)
    createdBy: Mapped[Optional["User"]] = relationship("User", remote_side=[id], back_populates="createdUsers", foreign_keys=[createdById])
    createdUsers: Mapped[List["User"]] = relationship("User", back_populates="createdBy", foreign_keys=[createdById])

    # dial_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # unique_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    HealthDataID : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("HealthData.id"), nullable=True)

    healthData : Mapped[Optional["HealthData"]] = relationship(back_populates="users",foreign_keys=[HealthDataID])

    healthDataAsOwner : Mapped["HealthData"] = relationship("HealthData", back_populates="user", foreign_keys="HealthData.UserID"  ,lazy="selectin")
    # Conversations
    conversations = relationship("Conversation", back_populates="creator")

    # Participant
    participants = relationship("Participant", back_populates="user", cascade="all, delete-orphan")

    # Messages
    messages_sent = relationship("Message", back_populates="sender", cascade="all, delete-orphan")
    

    # Template
    templates = relationship("Template", back_populates="creator", cascade="all, delete-orphan")

    #Sent Messages
    sent_messages: Mapped[list["SentMessages"]] = relationship(back_populates="created_by_user", foreign_keys="[SentMessages.createdBy]")

    # received messages

    messages_received: Mapped[list["SentMessages"]] = relationship(back_populates="user", foreign_keys="[SentMessages.user_id]")

    # Notifications
    notifications: Mapped[List["Notifications"]] = relationship("Notifications", back_populates="user", cascade="all, delete-orphan")

    mystreams: Mapped[List["LiveStream"]] = relationship(
        back_populates="owner", lazy="selectin"
    )

    received_sos: Mapped[list["SOS"]] = relationship(back_populates="receiver",foreign_keys="[SOS.receivedBy]")
    sent_sos: Mapped[list["SOS"]] = relationship(back_populates="sender",foreign_keys="[SOS.sentBy]")


    appointments_for_me: Mapped[List["Appointment"]] = relationship(back_populates="doctor", foreign_keys="Appointment.doctor_id")
    my_reffered_doctors : Mapped[List["Appointment"]] = relationship(back_populates="refferal_doctor", foreign_keys="Appointment.refferal_doc_id")
    
    family_as_mother: Mapped[List["Family"]] = relationship(back_populates="mother", foreign_keys="Family.motherId")

    family : Mapped[Optional["Family"]] = relationship("Family", back_populates="users", foreign_keys=[familyID])

    family_as_father: Mapped[List["Family"]] = relationship(back_populates="father", foreign_keys="Family.fatherId")

    family_requests: Mapped[List["FamilyRequests"]] = relationship(back_populates="user", foreign_keys="FamilyRequests.userId", lazy="selectin")

    user_name : Mapped[str] = mapped_column(String, nullable=True, index=True, unique=True)

    zone_id : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("zone.id"), nullable=True)


    __table_args__ = (
        UniqueConstraint("phone", "roleId"),
    )


class UserEntity(Base):
    __tablename__ = "user_entity"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id"), nullable=False)
    entity_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False)
    type : Mapped[str] = mapped_column(String, nullable=False)
    leftAt : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


class UserHandledBy(Base):
    __tablename__ = "user_handled_by"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id"), nullable=False)
    handled_by : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id"), nullable=False)
    type : Mapped[str] = mapped_column(String, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


class Account(Base):
    __tablename__ = "Account"

    id: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    userId: Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    providerAccountId: Mapped[str] = mapped_column(String, nullable=False)
    refresh_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    access_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    expires_at: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    token_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    scope: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    id_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    session_state: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("provider", "providerAccountId", name="provider_providerAccountId"),
    )


    # user: Mapped["User"] = relationship("User", back_populates="Account")


class Session(Base):
    __tablename__ = "Session"

    id: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    sessionToken: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    userId: Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    expires: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationships
    # user: Mapped["User"] = relationship("User", back_populates="Session")


class VerificationToken(Base):
    __tablename__ = "VerificationToken"

    identifier: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    expires: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    __table_args__ = (
    UniqueConstraint("identifier", "token", name="identifier_token"),
    )


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    titleIcon: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    titleHref: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    parent: Mapped[str] = mapped_column(String, nullable=False)
    parentIcon: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    parentHref: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True, index=True)
    data : Mapped[JSON] = mapped_column(JSON, nullable=True)
    slug: Mapped[str] = mapped_column(String, nullable=False, default="")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    permissions: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    createdBy: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_role_creator"), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    defaultSubscription = mapped_column(UUID(as_uuid=True), ForeignKey("subscription_plan.id"), nullable=True)
    
    entity : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("entity.id"), nullable=True)

    # Relationships
    users: Mapped[List["User"]] = relationship("User", back_populates="role", foreign_keys="User.roleId")
    createdByUser: Mapped[Optional["User"]] = relationship("User", back_populates="createdRoles", foreign_keys=[createdBy])



class OTP(Base):
    __tablename__ = 'otps'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    otp: Mapped[str] = mapped_column(String(6), nullable=False)
    phone: Mapped[str] = mapped_column(String(254), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    expiresAt: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5))



class ContentType(Base):
    __tablename__ = "content_types"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contentType : Mapped[str] = mapped_column(String) 
    category : Mapped[str] = mapped_column(String, nullable=True) 
    createdBy :Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_content_type_creator"), nullable=True)
    createdAt : Mapped[DateTime] = mapped_column(TIMESTAMP, server_default=func.now())
    roleId :Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id"))
    entityId :Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=True)
    isDeleted: Mapped[bool] = mapped_column(Boolean, nullable=True)

    users = relationship("User", foreign_keys=[createdBy])
    
    

class Content(Base):
    __tablename__ = "contents"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title : Mapped[str] = mapped_column(String)
    description : Mapped[str] = mapped_column(String)
    route : Mapped[str] = mapped_column(String, nullable=True, unique=True, index=True)
    visible : Mapped[bool] = mapped_column(Boolean, default=True)
    typeid : Mapped[int] = mapped_column(ForeignKey("content_types.id"), nullable=True)
    imageurl : Mapped[str] = mapped_column(String, nullable=True)
    videoUrl : Mapped[str] = mapped_column(String, nullable=True)
    createdby : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_content_creator"), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    viewType : Mapped[str] = mapped_column(String)
    pregnancyWeek: Mapped[int] = mapped_column(Integer, nullable=True)
    updatedAt : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category : Mapped[str] = mapped_column(String,default="common",nullable=True,index=True)

    users = relationship("User", foreign_keys=[createdby],lazy="selectin")

    content_types = relationship("ContentType", foreign_keys=[typeid],lazy="selectin")

    # BlogStats relationship (a content can have associated blog-stats records)
    # stats: Mapped[List["BlogStats"]] = relationship(
    #     "BlogStats",
    #     back_populates="content",
    #     foreign_keys="BlogStats.content_id",
    #     cascade="all, delete-orphan",
    #     lazy="selectin",
    # )

    viewCount : Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    likeCount : Mapped[int] = mapped_column(Integer,  default=0, nullable=True)
    shareCount : Mapped[int] = mapped_column(Integer, default=0 , nullable=True)
    commentCount : Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    actions: Mapped[list[dict]] = mapped_column(JSONB, nullable=True)
    expiration : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    pregnancyWeek : Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    tags: Mapped[List[str]] = mapped_column(ARRAY(String), default=list, nullable=True)

    isDeleted: Mapped[bool] = mapped_column(Boolean, nullable=True)







class LoginHistory(Base):  # Inherit from Base
    __tablename__ = "login_history"

    id : Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    ip : Mapped[str]  = mapped_column(String(20),nullable=True)
    country : Mapped[str] = mapped_column(String(30),nullable=True)
    region : Mapped[str] = mapped_column(String(20),nullable=True)
    city : Mapped[str] = mapped_column(String(50),nullable=True)
    user_id = mapped_column(UUID(as_uuid=True),ForeignKey("User.id", use_alter=True, name="fk_login_history_user"),nullable=False)
    user_type : Mapped[str] = mapped_column(String(20),nullable=True)
    user_os : Mapped[str] = mapped_column(String(20),nullable=True)
    device_info : Mapped[dict] = mapped_column(JSON)
    createdAt : Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    users  = relationship("User", foreign_keys=[user_id])



class Conversation(Base):
    __tablename__ = "conversations"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_group = mapped_column(Boolean, default=False)
    name = mapped_column(String, nullable=True)
    created_by = mapped_column(UUID(as_uuid=True), ForeignKey("User.id", use_alter=True, name="fk_conversation_creator"), nullable=False)
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", back_populates="conversations")
    participants = relationship("Participant", back_populates="conversation", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")



class Participant(Base):
    __tablename__ = "participants"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("User.id"), nullable=False)
    joinedAt = mapped_column(TIMESTAMP, server_default=func.now())
    role = mapped_column(String, default="member")

    conversation = relationship("Conversation", back_populates="participants")
    user = relationship("User", back_populates="participants")


class Message(Base):
    __tablename__ = "messages"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    sender_id = mapped_column(UUID(as_uuid=True), ForeignKey("User.id"), nullable=False)
    content = mapped_column(String, nullable=False)
    message_type = mapped_column(String, default="text")
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User", back_populates="messages_sent")

class Template(Base):
    __tablename__ = "templates"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = mapped_column(String(255), nullable=False)
    title = mapped_column(String(255), nullable=True)
    type = mapped_column(String(100), nullable=False, index=True)
    message = mapped_column(String, nullable=False)
    inputs = mapped_column(ARRAY(String), default=list)

    entity_id = mapped_column(UUID(as_uuid=True), ForeignKey("entity.id"), nullable=True, index=True)
    slug = mapped_column(String(100), nullable=True, index=True)

    data = mapped_column(JSON, nullable=True)


    createdBy = mapped_column(UUID(as_uuid=True), ForeignKey("User.id"), nullable=False)
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())

    sent_messages: Mapped[list["SentMessages"]] = relationship(back_populates="template")

    creator = relationship("User", back_populates="templates")



class Config(Base):
    __tablename__ = "configs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String,index=True, unique=True)
    description:Mapped[str] = mapped_column(String,nullable=True)
    key:Mapped[str] = mapped_column(String,nullable=True)
    message_body : Mapped[dict] = mapped_column(JSON)

class SentMessages(Base):
    __tablename__ = 'sent_messages'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)

    template_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("templates.id"), nullable=True
    )

    type: Mapped[str] = mapped_column(String(255), nullable=False)

    createdBy: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("User.id"), nullable=True
    )


    createdAt = mapped_column(TIMESTAMP, server_default=func.now())

    # ORM relationships
    created_by_user: Mapped["User"] = relationship(back_populates="sent_messages", foreign_keys=[createdBy])
    template: Mapped["Template | None"] = relationship(back_populates="sent_messages")

    to : Mapped[str]= mapped_column(String(255), nullable=True)
    values = mapped_column(ARRAY(String), default=list , nullable=True)
    api_response : Mapped[dict] = mapped_column(JSON, nullable=True)

    # new fields
    type : Mapped[str] = mapped_column(String(100), nullable=True)
    status : Mapped[str] = mapped_column(String(100), nullable=True, default="pending")
    user_id : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id"), nullable=True)

    user : Mapped[Optional["User"]] = relationship("User", back_populates="messages_received", foreign_keys=[user_id])

    # 

    weekInfoID : Mapped[Optional[int]] = mapped_column(ForeignKey("WeekWisePregnancyInfo.id"), nullable=True)
    appointmentID : Mapped[Optional[int]] = mapped_column(ForeignKey("Appointment.id"), nullable=True)
    immunizationScheduleID : Mapped[Optional[int]] = mapped_column(ForeignKey("ImmunizationSchedule.id"), nullable=True)
    ancCheckupDateID : Mapped[Optional[int]] = mapped_column(ForeignKey("ANCCheckupDates.id"), nullable=True)
    




class Token(Base):
    __tablename__ = 'tokens'
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    uid : Mapped[str] = mapped_column (String, nullable=False, index=True)
    token : Mapped[str] = mapped_column(String, nullable=False )

    __table_args__ = (
        UniqueConstraint("uid", "token"),
    )



class Notifications(Base):
    __tablename__ = 'notification'
    id : Mapped[int] = mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    user_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("User.id"), nullable=False,index=True
    )
    title : Mapped[str] = mapped_column(String(255), nullable=False)
    message : Mapped[str] = mapped_column(String(255), nullable=False)
    createdAt : Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(),index=True)
    is_read : Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="notifications")



# Translations

class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False,index=True)
    short: Mapped[str] = mapped_column(String(100), unique=True, nullable=False,index=True)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    translations: Mapped[list["TranslatedWord"]] = relationship(
        back_populates="language", cascade="all, delete-orphan"
    )


class OriginalWord(Base):
    __tablename__ = "original_words"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False, unique=True,index=True)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    translations: Mapped[list["TranslatedWord"]] = relationship(
        back_populates="original_word", cascade="all, delete-orphan"
    )

class TranslatedWord(Base):
    __tablename__ = "translated_words"
    __table_args__ = (
        UniqueConstraint("original_word_id", "language_id", name="uix_original_language"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    original_word_id: Mapped[int] = mapped_column(ForeignKey("original_words.id"), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)

    original_word: Mapped[OriginalWord] = relationship(back_populates="translations")
    language: Mapped[Language] = relationship(back_populates="translations")


class Enquiries(Base):
    __tablename__ = "enquiries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data : Mapped[dict] = mapped_column(JSON)


class SubscriptionType(Base):
    __tablename__ = "subscription_type"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name : Mapped[str] = mapped_column(String)
    order : Mapped[int] = mapped_column(Integer)
    role_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False, index=True
    )
    permissions: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)

    entity_id : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("entity.id"), nullable=True)

    deletedAt : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    subscription_plans: Mapped[list["SubscriptionPlan"]] = relationship(
        back_populates="subscription_type",lazy="selectin"
    )

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plan"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name : Mapped[str] = mapped_column(String)
    description : Mapped[str] = mapped_column(String)
    duration: Mapped[int] = mapped_column(Integer, default=0)
    recurringType = mapped_column(String)
    price : Mapped[int] = mapped_column(Integer,default=0)
    order : Mapped[int] = mapped_column(Integer)
    image : Mapped[str] = mapped_column(String)
    moneySymbol : Mapped[str] = mapped_column(String(1))
    details : Mapped[List[str]] = mapped_column(ARRAY(String))
    features : Mapped[List[str]] = mapped_column(ARRAY(String),nullable=True)
    features_not_available : Mapped[List[str]] = mapped_column(ARRAY(String),nullable=True)
    permissions : Mapped[List[str]] = mapped_column(ARRAY(String),nullable=True)

    recurring_plan_id : Mapped[Optional[str]] = mapped_column(String, nullable=True)


    durationType : Mapped[str] = mapped_column(String, default="month", nullable=True)

    deletedAt : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    subscription_type_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("subscription_type.id"))

    subscription_type: Mapped["SubscriptionType"] = relationship(
        back_populates="subscription_plans", lazy="selectin"
    )

    transactions: Mapped[List["Transactions"]] = relationship(
        back_populates="subscription_plan", lazy="selectin"
    )

    usersubs: Mapped[List["UserSubscription"]] = relationship(
        back_populates="plan", lazy="selectin"
    )


    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=True)

    entity: Mapped["Entity"] = relationship(
        "Entity",
        back_populates="subscription_plans",
        lazy="selectin",
    )

    hidden : Mapped[bool] = mapped_column(Boolean, default=False , nullable=True)


class UserSubscription(Base):
    __tablename__ = "userSubscription"
    id: Mapped[int] = mapped_column(Integer,primary_key = True, autoincrement= True)
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id"), nullable=False,index=True)
    subscription_plan_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("subscription_plan.id"), nullable=False)
    payment_type : Mapped[str] = mapped_column(String)
    payment : Mapped[dict] = mapped_column(JSON)
    start_date : Mapped[datetime] = mapped_column(TIMESTAMP,server_default= func.now())
    expiry_date : Mapped[datetime] = mapped_column(DateTime)
    
    plan: Mapped["SubscriptionPlan"] = relationship(
        back_populates="usersubs", lazy="selectin"
    )

class Apps(Base):
    __tablename__ = "apps"

    id: Mapped[str] = mapped_column(String,primary_key=True,index=True)
    logo :  Mapped[str] = mapped_column(String,nullable=True)
    name : Mapped[str] = mapped_column(String,nullable=False)
    data : Mapped[dict] = mapped_column(JSON)
    allowedRoles  = mapped_column(ARRAY(String),nullable=True,default=[])
    baseUrl = mapped_column(String,nullable=True,default="")


class Transactions(Base):
    __tablename__ = "transactions"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    completed:Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    pending:Mapped[Boolean] = mapped_column(Boolean,default=True)
    userSubscription_id:Mapped[int] = mapped_column(ForeignKey("userSubscription.id"),nullable=True)
    plan_id:Mapped[uuid.UUID] = mapped_column(ForeignKey("subscription_plan.id"))

    user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id"))

    
    paymentProvider:Mapped[String] = mapped_column(String)
    paymentData:Mapped[String] = mapped_column(JSON,nullable=True)

    createdAt = mapped_column(TIMESTAMP, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    adline1: Mapped[str] = mapped_column(String, nullable=True)
    adline2: Mapped[str] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=True)
    pincode: Mapped[str] = mapped_column(String, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=True)
    country: Mapped[str] = mapped_column(String, nullable=True)


    subscription_plan: Mapped["SubscriptionPlan"] = relationship(
        back_populates="transactions", lazy="selectin"
    )



class ContentStats(Base):
    __tablename__ = "content_stats"
    id: Mapped[int] = mapped_column(Integer,primary_key = True, autoincrement= True)
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id"), nullable=False)
    content_id : Mapped[int] = mapped_column(ForeignKey("contents.id"), nullable=False)
    type : Mapped[str] = mapped_column(String,index=True)
    comment : Mapped[str] = mapped_column(String, nullable=True)

    createdAt = mapped_column(TIMESTAMP, server_default=func.now())


class CallHistory(Base):
    __tablename__ = "call_history"
    id: Mapped[int] = mapped_column(Integer,primary_key = True, autoincrement= True)
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id"), nullable=False)
    reciver_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id"), nullable=False)
    duration : Mapped[int] = mapped_column(Integer)
    status: Mapped[bool] = mapped_column(Boolean)
    type : Mapped[str] = mapped_column(String,index=True)
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())


class LiveStream(Base):
    __tablename__ = "LiveStream"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    ownerID : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id"), nullable=False)
    title : Mapped[str] = mapped_column(String)
    slug : Mapped[str] = mapped_column(String,nullable=True)
    description : Mapped[str] = mapped_column(String)
    chatStatus: Mapped[bool] = mapped_column(Boolean)
    startTime: Mapped[datetime] = mapped_column(DateTime)
    status : Mapped[str] = mapped_column(String, default="Scheduled")
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())
    endTime: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    enabled : Mapped[bool] = mapped_column(Boolean, default=True)

    owner: Mapped["User"] = relationship(
        back_populates="mystreams", lazy="selectin"
    )

class Entity(Base):
    __tablename__ = "entity"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    route : Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    hours: Mapped[int] = mapped_column(Integer, nullable=False)

    availableHours : Mapped[str] = mapped_column(String, nullable=True)

    image: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    # Foreign key for entityType relationship
    entity_type_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("entityType.id"), nullable=False)
    # Relationship to entityType
    entity_type = relationship("EntityType", back_populates="entities")
    ownerEntityId: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=True)
    modules: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    adressline1: Mapped[str] = mapped_column(String, nullable=False)
    adressline2: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)
    pincode: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[str] = mapped_column(String, nullable=False)
    longitude: Mapped[str] = mapped_column(String, nullable=False)

    logoImage: Mapped[str] = mapped_column(String, nullable=False)
    bannerImage: Mapped[str] = mapped_column(String, nullable=False)

    data: Mapped[dict] = mapped_column(JSON, nullable=False)

    website: Mapped[str] = mapped_column(String, nullable=False)
    contact: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    themeinfo: Mapped[dict] = mapped_column(JSON, nullable=False)

    defaultDoctorId: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id"), nullable=True)
    defaultHealthWorkerId: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id"), nullable=True)
    defaultLabWorkerId: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id"), nullable=True)
    defaultNurseId: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id"), nullable=True)

    isDeleted: Mapped[bool] = mapped_column(Boolean, nullable=True)
    

    createdBy: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_entity_creator"), nullable=True)

    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=True)

    users : Mapped[List["User"]] = relationship("User", back_populates="userEntity", foreign_keys="User.entity")

    zone_id : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("zone.id"), nullable=True)
    zone : Mapped[Optional["Zone"]] = relationship("Zone", lazy="selectin")

    wallet_balance : Mapped[float] = mapped_column(Float, nullable=True, default=0.0)

    #dynamic razorpay fields
    razorpay_key_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    razorpay_key_secret: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    razorpay_recurring_plan_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    subscription_plans: Mapped[List["SubscriptionPlan"]] = relationship(
    "SubscriptionPlan",
    back_populates="entity",
    lazy="selectin",)

    # landing_pages: Mapped[List["LandingPage"]] = relationship(
    # "LandingPage",
    # back_populates="entity")
    

    



class Zone(Base):
    __tablename__ = "zone"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=True)
    entities : Mapped[List["Entity"]] = relationship("Entity", back_populates="zone", foreign_keys="Entity.zone_id")

class EntityType(Base):
    __tablename__ = "entityType"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Relationship with entity - one entityType can have many entities
    entities: Mapped[list["Entity"]] = relationship("Entity", back_populates="entity_type")


class SOS(Base):
    __tablename__ = "SOS"

    id :Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sentBy : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_sos_creator"), nullable=True)
    lat : Mapped[float] = mapped_column(Float, nullable=True)
    lng : Mapped[float] = mapped_column(Float, nullable=True)
    reason : Mapped[str]  = mapped_column(String, nullable=True)
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())
    notificationId : Mapped[str] = mapped_column(String, nullable=True)
    
    receivedBy : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_sos_reciever"), nullable=True)
    receiver: Mapped[User] = relationship(back_populates="received_sos",foreign_keys=[receivedBy],lazy="selectin")
    sender: Mapped[User] = relationship(back_populates="sent_sos",foreign_keys=[sentBy],lazy="selectin")
    completedAt : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)





class HealthData(Base):
    __tablename__ = "HealthData"
    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    UserID : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_healthdata_user"), nullable=True)
    height : Mapped[float] = mapped_column(Float, nullable=True)
    weight : Mapped[float] = mapped_column(Float, nullable=True)
    rch_id : Mapped[String] = mapped_column(String, nullable=True, index=True)
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())
    recoveryPhone : Mapped[str] = mapped_column(String, nullable=True)
    recoveryEmail : Mapped[str] = mapped_column(String, nullable=True)

    healthStatus : Mapped[Optional[str]] = mapped_column(String, nullable=True)

    lmpDate : Mapped[datetime]  = mapped_column(DateTime, nullable=True)
    averageCycle : Mapped[float] = mapped_column(Float, nullable=True)
    cycleType : Mapped[str] = mapped_column(String, nullable=True)
    edDate : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    pregnancyStatus : Mapped[Optional[str]] = mapped_column(String, nullable=True)
    lastDeliveryDate : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user : Mapped["User"] = relationship(back_populates="healthDataAsOwner", foreign_keys=[UserID],lazy="selectin")

    users : Mapped[List["User"]] = relationship(back_populates="healthData", foreign_keys="User.HealthDataID",lazy="selectin")

    pregnancies : Mapped[List["Pregnancy"]] = relationship(back_populates="healthData")

    # Risk

    riskStatus : Mapped[Optional[str]] = mapped_column(String, nullable=True)

    riskUpdatedAt : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    flaggedComplications: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)

    overallHealth : Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    latestRiskData : Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    #  new fields for health data

    husbandName: Mapped[str] = mapped_column(String, nullable=True)
    husbandMobile: Mapped[str] = mapped_column(String, nullable=True)
    husbandImage : Mapped[str] = mapped_column(String, nullable=True)
    # husband_dob: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    pastIllness: Mapped[List[str]]= mapped_column(ARRAY(String), nullable=True, default=list)

    bleedingTime: Mapped[time] = mapped_column(Time, nullable=True)
    clottingTime: Mapped[time] = mapped_column(Time, nullable=True)
    vdrlResult: Mapped[str] = mapped_column(String, nullable=True)
    hbsagResult: Mapped[str] = mapped_column(String, nullable=True)
    hivResult: Mapped[str] = mapped_column(String, nullable=True)

    husbandVdrlResult: Mapped[str] = mapped_column(String, nullable=True)
    husbandHbsagResult: Mapped[str] = mapped_column(String, nullable=True)
    husbandHivResult: Mapped[str] = mapped_column(String, nullable=True)
    totalPregnancies: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    # default users to assist mother

    defaultDoctorId: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id"), nullable=True)
    defaultHealthWorkerId: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id"), nullable=True)
    defaultLabWorkerId: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id"), nullable=True)
    defaultNurseId: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id"), nullable=True)

    
    appointments : Mapped[List["Appointment"]] = relationship(
        "Appointment", back_populates="healthData", foreign_keys="Appointment.HealthDataID", lazy="selectin"
    )



    selfScreenings : Mapped[List["SelfScreening"]] = relationship(
        "SelfScreening", back_populates="healthData", foreign_keys="SelfScreening.HealthDataID", lazy="selectin"
    ) 

    dailyActivities : Mapped[List["DailyActivity"]] = relationship(
        "DailyActivity", back_populates="healthData", foreign_keys="DailyActivity.health_id", lazy="selectin"
    )

    userRequests : Mapped[List["UserRequest"]] = relationship(
        "UserRequest", back_populates="healthData", foreign_keys="UserRequest.healthID", lazy="selectin"
    )

    vitalsRecords : Mapped[List["VitalsRecord"]] = relationship(
        "VitalsRecord", back_populates="healthData", foreign_keys="VitalsRecord.health_id", lazy="selectin"
    )

class Family(Base):
    __tablename__ = "Family"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name : Mapped[str] = mapped_column(String, nullable=True)
    code :Mapped[str] = mapped_column(String, nullable=True)
    motherId : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_family_mother"), nullable=True)
    fatherId : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_family_father"), nullable=True)
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())
    createdBy : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_family_creator"), nullable=True)

    mother : Mapped["User"] = relationship(back_populates="family_as_mother", foreign_keys=[motherId],lazy="selectin")
    users : Mapped[List["User"]] = relationship("User", back_populates="family", foreign_keys="User.familyID",lazy="selectin")
    father : Mapped["User"] = relationship( back_populates="family_as_father", foreign_keys=[fatherId],lazy="selectin")

class FamilyRequests(Base):
    __tablename__ = "FamilyRequests"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_familyrequest_user"), nullable=True)
    familyId : Mapped[uuid.UUID] = mapped_column(ForeignKey("Family.id", use_alter=True, name="fk_familyrequest_family"), nullable=True)
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())
    expiresAt = mapped_column(TIMESTAMP, default=lambda: datetime.utcnow() + timedelta(days=1))
    status : Mapped[str] = mapped_column(String, nullable=True)
    user : Mapped["User"] = relationship("User", back_populates="family_requests", foreign_keys=[userId],lazy="selectin")
    



class FamilyMembers(Base):
    __tablename__ = "FamilyMembers"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userid: Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_familymember_user"), nullable=True)
    familyid: Mapped[uuid.UUID] = mapped_column(ForeignKey("Family.id", use_alter=True, name="fk_familymember_family"), nullable=True)
    relation: Mapped[str] = mapped_column(String, nullable=True)
    access_level : Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)




class TimeSlots(Base):

    __tablename__ = "TimeSlots"


    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctorId : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_timeslots_doctor"), nullable=True)
    available_day : Mapped[int] = mapped_column(Integer, nullable=False)  # 0 to 6 (Sunday to Saturday)
    available_from : Mapped[datetime] = mapped_column(DateTime, nullable=False)
    available_to : Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration : Mapped[str] = mapped_column(String, nullable=True)
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())

    appointments : Mapped[list["Appointment"]] = relationship(back_populates="timing", cascade="all, delete-orphan", foreign_keys="Appointment.timing_id")


class Holiday(Base):

    __tablename__ = "Holiday"
    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date : Mapped[datetime] = mapped_column(DateTime, nullable=False)
    DoctorId : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_holiday_doctor"), nullable=True)			


class Appointment(Base):
    __tablename__ = "Appointment"
        
    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,default=uuid.uuid4)		
    doctor_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('User.id'), nullable=True)
    doctor_name : Mapped[str] = mapped_column(String, nullable=True) # Legacy support

    HealthDataID: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('HealthData.id'), nullable=True) # Made nullable for simple bookings

    timing_id :Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('TimeSlots.id'), nullable=True)	
            
    appointment_date : Mapped[datetime] = mapped_column(DateTime, nullable=True)		
    appointment_time : Mapped[datetime] = mapped_column(DateTime, nullable=True) # Legacy support
    user_id : Mapped[str] = mapped_column(String, nullable=True) # Legacy support
            
    status :Mapped[str] = mapped_column(String, default="Scheduled", nullable=False)		
            
    reason :Mapped[str] = mapped_column(String, nullable=True)		
            
    created_at:Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)		
    updated_at : Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)		
            
    is_reffered :Mapped[bool] = mapped_column(Boolean, default=False)		
    refferal_doc_id:Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('User.id'), nullable=True)
    refferal_doc_name:Mapped[str] = mapped_column(String, nullable=True)		
            
    # after checkup		
    healthStatus:Mapped[str] = mapped_column(String, nullable=True)		
    checkup_date =  mapped_column(DateTime, nullable=True)		
    summary:Mapped[str] = mapped_column(String, nullable=True)
            
    next_appointment_id :Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('Appointment.id'), nullable=True) # Enable after Appointment Table migration
    next_appointment_date:Mapped[datetime] = mapped_column(DateTime, nullable=True)		
            
    # self_screening_id = mapped_column(Integer, nullable=True, index=True, unique=True)		

    doctor: Mapped["User"] = relationship("User", back_populates="appointments_for_me", foreign_keys=[doctor_id],lazy="selectin")

    timing: Mapped["TimeSlots"] = relationship("TimeSlots", back_populates="appointments", foreign_keys=[timing_id],lazy="selectin")

    refferal_doctor: Mapped["User"] = relationship("User", back_populates="my_reffered_doctors", foreign_keys=[refferal_doc_id],lazy="selectin")

    next_appointment: Mapped[Optional["Appointment"]] = relationship(back_populates="next_booked_appointments", remote_side=[id], foreign_keys=[next_appointment_id],lazy="selectin")
    next_booked_appointments : Mapped[List["Appointment"]] = relationship(back_populates="next_appointment",foreign_keys="Appointment.next_appointment_id")

    self_screening : Mapped[Optional["SelfScreening"]] = relationship("SelfScreening", back_populates="appointment", uselist=False, lazy="selectin")

    healthData : Mapped["HealthData"] = relationship("HealthData", back_populates="appointments", foreign_keys=[HealthDataID],lazy="selectin")

    riskStatus : Mapped[str] = mapped_column(String, default="Normal", nullable=True)

    reports : Mapped[List["Report"]] = relationship(
        "Report", back_populates="appointment", foreign_keys="Report.appointmentId", lazy="selectin"
    )

    ancCheckupDates : Mapped[List["ANCCheckupDates"]] = relationship(
        "ANCCheckupDates", back_populates="appointment", foreign_keys="ANCCheckupDates.appointment_id", lazy="selectin"
    )

    prescriptions : Mapped[List["Prescription"]] = relationship(
        "Prescription", back_populates="appointment", foreign_keys="Prescription.appointmentId", lazy="selectin"
    )

    type : Mapped[str] = mapped_column(String, default="General", nullable=True) 

class AppointmentSlots(Base):
    __tablename__ = "AppointmentSlots"
    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_appointmentslots_doctor"), nullable=True)
    date : Mapped[datetime] = mapped_column(DateTime, nullable=False)
    timeslotId : Mapped[uuid.UUID] = mapped_column(ForeignKey("TimeSlots.id", use_alter=True, name="fk_appointmentslots_timeslot"), nullable=True)
    appointmentId : Mapped[uuid.UUID] = mapped_column(ForeignKey("Appointment.id", use_alter=True, name="fk_appointmentslots_appointment"), nullable=True)
    is_booked : Mapped[bool] = mapped_column(Boolean, default=False)

class Pregnancy(Base):
    __tablename__ = "Pregnancy"
    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lmpDate : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    edDate : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    health_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id", use_alter=True, name="fk_pregnancy_healthdata"), nullable=True)
    deliveryDate : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    rch_id : Mapped[str] = mapped_column(String, nullable=True, index=True)

    status : Mapped[str] = mapped_column(String, default="active", nullable=True) # active , delivered , aborted , miscarraige , stillbirth , neonatal death , mother_deceased
    createdBy : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id", use_alter=True, name="fk_pregnancy_creator"), nullable=True)

    healthData : Mapped[HealthData] = relationship(back_populates="pregnancies")

    birth_records : Mapped[List["BirthRecord"]] = relationship(back_populates="pregnancy")

    checkup_dates : Mapped[List["ANCCheckupDates"]] = relationship(
        "ANCCheckupDates", back_populates="pregnancy", foreign_keys="ANCCheckupDates.pregnancy_id", lazy="selectin"
    )

    # 
    registerWithin12Weeks: Mapped[bool] = mapped_column(Boolean,nullable=True, default=False)  

    # flagging risk
    # overallVitals : Mapped[dict] = mapped_column(JSON, nullable=True)


    # flaggedData : Mapped[dict] = mapped_column(JSON, nullable=True)

    # Additional fields for anc

    methodOfConception: Mapped[str] = mapped_column(String, nullable=True)
    gravidity: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of times pregnant
    parity: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of times given birth
    livingChildren: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of living children
    abortions: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of abortions
    stillBirths: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of stillbirths
    miscarriages: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of miscarriages

    obstetricCode: Mapped[str] = mapped_column(String, nullable=True)  # Obstetric code for the pregnancy

    mrmbsEligible: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)  # Whether the mother is eligible for MRMBs scheme

    motherAge: Mapped[int] = mapped_column(Integer, nullable=True)  # Mother's age at the time of pregnancy
    fatherAge: Mapped[int] = mapped_column(Integer, nullable=True)  # Father's age at the time of pregnancy


    createdAt : Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    completedAt : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    deliveryConductedAt : Mapped[str] = mapped_column(String,nullable=True) # Hospital/Clinic/Home

    admittedAt : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Date of admission for delivery
    dischargedAt : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Date of discharge after delivery

    deceasedAt : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Date of death if applicable
    causeOfDeath : Mapped[Optional[str]] = mapped_column(String, nullable=True)


    mother_report_checklists : Mapped[List["MotherReportCheckList"]] = relationship(
        "MotherReportCheckList", back_populates="pregnancy", foreign_keys="MotherReportCheckList.pregnancy_id", lazy="selectin"
    )

    immunization_records : Mapped[List["MotherImmunizationRecord"]] = relationship(
        "MotherImmunizationRecord", back_populates="pregnancy", foreign_keys="MotherImmunizationRecord.pregnancy_id", lazy="selectin"
    )



class ANCCheckupDates(Base):
    __tablename__ = "ANCCheckupDates"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date : Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pregnancy_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Pregnancy.id", use_alter=True, name="fk_anccheckupdates_ancrecord"))
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())
    appointment_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Appointment.id", use_alter=True, name="fk_anccheckupdates_appointment"), nullable=True)
    pregnancy : Mapped["Pregnancy"] = relationship(back_populates="checkup_dates", lazy="selectin")
    month : Mapped[int] = mapped_column(Integer, nullable=True)
    completedDate : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    appointment : Mapped[Optional["Appointment"]] = relationship(
        "Appointment", back_populates="ancCheckupDates", foreign_keys=[appointment_id], lazy="selectin"
    )

    todoId : Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("ToDoInfo.id", use_alter=True, name="fk_anccheckupdates_todo"), nullable=True)

class BirthRecord(Base):
    __tablename__ = "BirthRecord"
    id :Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deliveryDate : Mapped[datetime] = mapped_column(DateTime, nullable=False)
    condition : Mapped[str] = mapped_column(String, nullable=True) #live , deceased , neonatal death
    gender : Mapped[str] = mapped_column(String, nullable=True)
    weight : Mapped[float] = mapped_column(Float, nullable=True)
    entity_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("entity.id", use_alter=True, name="fk_birthrecord_entity"), nullable=True)
    photo : Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    video :  Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    blood_group : Mapped[str] = mapped_column(String, nullable=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    typeOfDelivery : Mapped[str] = mapped_column(String, nullable=False)

    pregnancy_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Pregnancy.id", use_alter=True, name="fk_birthrecord_pregnancy"),nullable=True)

    pregnancy : Mapped["Pregnancy"] = relationship(back_populates="birth_records",lazy="selectin")

    createdBy : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id", use_alter=True, name="fk_birthrecord_creator"), nullable=True)
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())

    health_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id", use_alter=True, name="fk_birthrecord_healthdata"), nullable=True)

    profilePic : Mapped[str] = mapped_column(String, nullable=True)  # URL of the baby's profile picture

    # 

    complications : Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True, default=list)
    infantId : Mapped[str] = mapped_column(String, nullable=True,)

    height : Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    delayedCordClamping : Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)  # Whether delayed cord clamping was done
    skinToSkinContact : Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)  # Whether skin-to-skin contact was done
    breastFeedingInHalfHour : Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)  # Whether exclusive breastfeeding was initiated


    dischargeDate : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Date of discharge from the hospital

    vitaminKDate : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Date of Vitamin K administration

    deliveryConductedAt : Mapped[str] = mapped_column(String,nullable=True) # Hospital/Clinic/Home


    deceasedAt : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Date of death if applicable
    causeOfDeath : Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # gravidity: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of times pregnant
    # parity: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of times given birth
    # livingChildren: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of living children
    # abortions: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of abortions
    # stillBirths: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of stillbirths
    # miscarriages: Mapped[int] = mapped_column(Integer, nullable=True, default=0)  # Number of miscarriages

    # obstetricCode: Mapped[str] = mapped_column(String, nullable=True)  # Obstetric code for the pregnancy

    # mrmbsEligible: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)  # Whether the mother is eligible for MRMBs scheme
        

class Baby(Base):
    __tablename__ = "Baby"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name : Mapped[str] = mapped_column(String, nullable=False)
    birth_record_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("BirthRecord.id", use_alter=True, name="fk_baby_birthrecord"), nullable=True)
    



class ReportType(Base):
    __tablename__ = "ReportType"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name : Mapped[str] = mapped_column(String, nullable=False)


class Report(Base):
    __tablename__ = 'Report'
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_type : Mapped[str] = mapped_column(String(50), nullable=False)
    detail : Mapped[dict] = mapped_column(JSON, nullable=True)
    healthDataID : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id", use_alter=True, name="fk_report_healthdata"), nullable=True)
    imageUrl : Mapped[str] = mapped_column(String(500), nullable=True)
    description : Mapped[str] = mapped_column(String(1000), nullable=True)
    isLab : Mapped[bool] = mapped_column(Boolean, default=True)
    labId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("entity.id", use_alter=True, name="fk_report_lab"), nullable=True)
    createdAt = mapped_column(TIMESTAMP, server_default=func.now())
    appointmentId : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("Appointment.id", use_alter=True, name="fk_report_appointment"), nullable=True)
    createdBy : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_report_createdby"), nullable=True)

    appointment : Mapped[Optional["Appointment"]] = relationship(
        "Appointment", back_populates="reports", foreign_keys=[appointmentId], lazy="selectin"
    )





class SelfScreening(Base):
    __tablename__ = 'SelfScreening'

    id :Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    HealthDataID : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id", use_alter=True, name="fk_report_healthdata"), nullable=True)

    params: Mapped[dict] = mapped_column(JSON, nullable=True)
    hemoglobinId : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("Report.id",ondelete="SET NULL", use_alter=True, name="fk_selfscreening_hemoglobin"), nullable=True)
    urineTestId : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("Report.id",ondelete="SET NULL", use_alter=True, name="fk_selfscreening_urine"), nullable=True)
    glucoseId : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("Report.id",ondelete="SET NULL", use_alter=True, name="fk_selfscreening_glucose"), nullable=True)
    fetalTestId : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("Report.id",ondelete="SET NULL", use_alter=True, name="fk_selfscreening_fetal"), nullable=True)
    ultrasoundId : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("Report.id",ondelete="SET NULL", use_alter=True, name="fk_selfscreening_ultrasound"), nullable=True)

    createdAt : Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    updatedAt : Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    appointmentID : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("Appointment.id", use_alter=True, name="fk_selfscreening_appointment"), nullable=True)

    createdBy : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_selfscreening_createdby"), nullable=True)
    createdFor : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_selfscreening_createdfor"), nullable=True)

    appointment : Mapped["Appointment"] = relationship(
        back_populates="self_screening", foreign_keys=[appointmentID], lazy="selectin"
    )


    healthData : Mapped["HealthData"] = relationship(
        back_populates="selfScreenings", foreign_keys=[HealthDataID], lazy="selectin"
    )

    vitalRecord : Mapped[Optional["VitalsRecord"]] = relationship(
        "VitalsRecord", back_populates="selfScreening", uselist=False, foreign_keys="VitalsRecord.selfScreeningID", lazy="selectin"
    )    




class Cry(Base):

    __tablename__ = "Cry"
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text : Mapped[str] = mapped_column(String(500), nullable=False)
    audioLink : Mapped[str] = mapped_column(String, nullable=False)
    userId : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_cry_user"), nullable=True)
    babyId : Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("Baby.id", use_alter=True, name="fk_cry_baby"), nullable=True)
    createdAt:Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    save:Mapped[bool] = mapped_column(Boolean, default=False)


class DeviceType(Base):

    __tablename__ = "DeviceType"
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[str] = mapped_column(String, nullable=False)
    entityId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("entity.id", use_alter=True, name="fk_device_type_entity"), nullable=True)
    createdBy : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id", use_alter=True, name="fk_device_type_createdby"), nullable=True)
    createdAt:Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    

class Devices(Base):
    __tablename__ = "Devices"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_type_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("DeviceType.id", use_alter=True, name="fk_devices_devicetype"), nullable=False)
    entityId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("entity.id", use_alter=True, name="fk_devices_entity"), nullable=True)
    userId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id", use_alter=True, name="fk_devices_createdby"), nullable=True)


class DeviceData(Base):

    __tablename__ = "DeviceData"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deviceId:Mapped[uuid.UUID] = mapped_column(ForeignKey("Devices.id", use_alter=True, name="fk_devicedata_device"), nullable=False)
    value:Mapped[dict] = mapped_column(JSON, nullable=False)
    createdAt:Mapped[datetime] = mapped_column(DateTime, server_default=func.now())



class MedicineType(Base):
    __tablename__ = "MedicineType"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String, nullable=False)
    entityId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("entity.id", use_alter=True, name="fk_prescriptiontype_entity"), nullable=True)
    createdBy : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id", use_alter=True, name="fk_prescriptiontype_createdby"), nullable=True)
    createdAt:Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Medicines(Base):
    __tablename__ = "Medicines"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String, nullable=False)
    price:Mapped[int] = mapped_column(Integer, nullable=False)
    description:Mapped[str] = mapped_column(String, nullable=False)

    used_for : Mapped[List[String]] = mapped_column(ARRAY(String))
    image_url:Mapped[str] = mapped_column(String, nullable=True)
    createdBy :Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_prescription_createdby"), nullable=True)
    medicine_type_id :Mapped[int] = mapped_column(ForeignKey("MedicineType.id"), nullable=False)
    

class FeatureName(Base):
    __tablename__ = "FeatureName"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[str] = mapped_column(String, nullable=False)
    entityId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("entity.id", use_alter=True, name="fk_featurename_entity"), nullable=True)
    permission_name :Mapped [str] = mapped_column(String, nullable=False)



class BankAccount(Base):
    __tablename__ = "BankAccount"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    AccountHolderName:Mapped[str] = mapped_column(String, nullable=False)
    bankName:Mapped[str] = mapped_column(String, nullable=False)
    branch :Mapped[str] = mapped_column(String, nullable=False)
    accountNumber:Mapped[str] = mapped_column(String, nullable=False)
    ifscCode:Mapped[str] = mapped_column(String, nullable=False)
    userId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id", use_alter=True, name="fk_bankaccount_createdby"), nullable=True)

class UpdateData(Base):
    __tablename__ = "UpdateData"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_name:Mapped[str] = mapped_column(String, nullable=False, index=True)
    data_id:Mapped[str] = mapped_column(String, nullable=False, index=True)
    old_data:Mapped[dict] = mapped_column(JSON, nullable=False)
    new_data:Mapped[dict] = mapped_column(JSON, nullable=True)
    is_deleted:Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    updated_by:Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_updatedata_updatedby"), nullable=True)
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Prescription(Base):
    __tablename__ = "Prescription"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    health_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id", use_alter=True, name="fk_prescription_healthdata"), nullable=True)
    appointmentId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Appointment.id", use_alter=True, name="fk_prescription_appointment"), nullable=True)
    description:Mapped[str] =  mapped_column(String, nullable=False)
    imageUrl:Mapped[str] = mapped_column(String, nullable=True)
    createdAt:Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    medicines: Mapped[List["PrescriptionMedicine"]] = relationship(back_populates="prescription", cascade="all, delete-orphan", lazy="selectin")
    appointment: Mapped[Optional["Appointment"]] = relationship(
        "Appointment", back_populates="prescriptions", foreign_keys=[appointmentId], lazy="selectin"
    )



class PrescriptionMedicine(Base):
    __tablename__ = "PrescriptionMedicine"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prescriptionId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Prescription.id", use_alter=True, name="fk_prescriptionmedicine_prescription"), nullable=True)
    medicineId : Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Medicines.id", use_alter=True, name="fk_prescriptionmedicine_medicine"), nullable=True)
    medicineName : Mapped[str] = mapped_column(String, nullable=False)
    dosage :Mapped[str] = mapped_column(String, nullable=False)
    timings :Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    durationDays :Mapped[int] = mapped_column(Integer, nullable=False)
    notes :Mapped[str] = mapped_column(String, nullable=True)

    prescription : Mapped["Prescription"] = relationship(back_populates="medicines", foreign_keys=[prescriptionId] ,lazy="selectin")

    medicine_timings: Mapped[List["PrescriptionMedicineTiming"]] = relationship(back_populates="medicine", cascade="all, delete-orphan", lazy="selectin")


class PrescriptionMedicineTiming(Base):
    __tablename__ = "PrescriptionMedicineTiming"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prescriptionMedicineId: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("PrescriptionMedicine.id", use_alter=True, name="fk_prescriptionmedicine_timing_prescription"),
        nullable=True
    )
    dateTime: Mapped[datetime] = mapped_column(DateTime)
    medicineTakenTime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    medicine : Mapped["PrescriptionMedicine"] = relationship(
        back_populates="medicine_timings",
        lazy="selectin",
        foreign_keys=[prescriptionMedicineId]
    )

class DailyActivity(Base):

    __tablename__ = "DailyActivity"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    health_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=False), ForeignKey("HealthData.id", use_alter=True, name="fk_dailyactivity_healthdata"), nullable=True)
    feeling :Mapped[str] = mapped_column(String, nullable=True)
    exercises : Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    glassOfWater : Mapped[int] = mapped_column(Integer, nullable=True)
    medicine : Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    bedTime : Mapped[time] = mapped_column(Time, nullable=True)
    wakeupTime : Mapped[time] = mapped_column(Time, nullable=True)
    sleepDuration : Mapped[int] = mapped_column(Integer, nullable=True)
    symptoms : Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    date : Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt : Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    vitalData : Mapped[JSONB] = mapped_column(JSONB, nullable=True)
    riskStatus : Mapped[str] = mapped_column(String, default="Normal", nullable=True)

    healthData : Mapped["HealthData"] = relationship(
        "HealthData", back_populates="dailyActivities", foreign_keys=[health_id], lazy="selectin"
    )

    vitalsRecord : Mapped[Optional["VitalsRecord"]] = relationship(
        "VitalsRecord", back_populates="dailyActivity", uselist=False, foreign_keys="VitalsRecord.dailyActivityID", lazy="selectin"
    )
    
    __table_args__ = (
        UniqueConstraint("health_id", "date", name="uq_dailyactivity_health_date"), 
    )
    
class VitalsRecord(Base):
    __tablename__ = "VitalsRecord"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    health_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id", ondelete="CASCADE", use_alter=True, name="fk_vitalsrecord_healthdata"), nullable=True, index=True)
    bloodPressureH: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bloodPressureL: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bloodSaturation: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    temperature: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    temperatureMetric: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    heartRate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bloodGlucose: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bloodGlucoseUnit: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    bmiHeight: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bmiWeight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    respiratoryRate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    hrv: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    hB: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    flagged_complications: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True, default=list)
    riskStatus: Mapped[str] = mapped_column(String, default="LOW", nullable=True)
    riskData : Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    selfScreeningID: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("SelfScreening.id", use_alter=True, name="fk_vitalsrecord_selfscreening", ondelete="CASCADE"), nullable=True, unique=True)
    dailyActivityID : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("DailyActivity.id", use_alter=True, name="fk_vitalsrecord_dailyactivity", ondelete="CASCADE"), nullable=True, unique=True)

    report_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Report.id", use_alter=True, name="fk_vitalsrecord_report", ondelete="CASCADE"), nullable=True)

    selfScreening: Mapped[Optional["SelfScreening"]] = relationship(
        "SelfScreening", back_populates="vitalRecord", uselist=False, foreign_keys=[selfScreeningID], lazy="selectin"
    )

    dailyActivity : Mapped[Optional["DailyActivity"]] = relationship(
        "DailyActivity", back_populates="vitalsRecord", uselist=False, foreign_keys=[dailyActivityID], lazy="selectin"
    )

    healthData : Mapped[Optional["HealthData"]] = relationship("HealthData", back_populates="vitalsRecords", foreign_keys=[health_id], lazy="selectin")



class VitalsStream(Base):
    __tablename__ = "VitalsStream"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    health_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id", use_alter=True, name="fk_vitalstream_healthdata"), nullable=True,index=True)
    key : Mapped[str] = mapped_column(String, nullable=False,index=True)
    value : Mapped[str] = mapped_column(String, nullable=False)
    unit : Mapped[str] = mapped_column(String, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())



class LabReportType(Base):
    __tablename__ = "LabReportType"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:Mapped[str] = mapped_column(String, nullable=False)
    entityID : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("entity.id", use_alter=True, name="fk_labreporttype_entity"), nullable=True)

class UserRequest(Base):
    
    __tablename__ = "UserRequest"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    healthID : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id", use_alter=True, name="fk_request_healthdata"), nullable=True)
    reason : Mapped[str] = mapped_column(String, nullable=True)
    priority : Mapped[str] = mapped_column(String, nullable=False)
    status : Mapped[str] = mapped_column(String, nullable=False)
    entityID : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("entity.id", use_alter=True, name="fk_request_entity"), nullable=True)
    toUserID : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id", use_alter=True, name="fk_request_touser"), nullable=True)
    appointmentID : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Appointment.id", use_alter=True, name="fk_request_appointment"), nullable=True)
    reportID : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Report.id", use_alter=True, name="fk_request_report"), nullable=True)
    requestType : Mapped[str] = mapped_column(String, nullable=False)
    name : Mapped[str] = mapped_column(String, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt : Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    healthData: Mapped[Optional["HealthData"]] = relationship("HealthData", back_populates="userRequests")

class RiskRecords(Base):
    __tablename__ = "RiskRecords"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    health_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id", use_alter=True, name="fk_riskrecords_healthdata"), nullable=True)
    risk_type: Mapped[str] = mapped_column(String, nullable=False)
    risk_level: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    cured: Mapped[bool] = mapped_column(Boolean, default=False)
    report_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Report.id", use_alter=True, name="fk_riskrecords_report", ondelete="CASCADE"), nullable=True)
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Appointment.id", use_alter=True, name="fk_riskrecords_appointment", ondelete="CASCADE"), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())



class MotherImmunizationRecord(Base):
    __tablename__ = "MotherImmunizationRecord"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    health_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id", use_alter=True, name="fk_immunizationrecord_healthdata"), nullable=True)
    pregnancy_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Pregnancy.id", use_alter=True, name="fk_immunizationrecord_pregnancy"), nullable=True)
    vaccine_name : Mapped[str] = mapped_column(String, nullable=False)
    expected_date : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    vaccination_date : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    required : Mapped[bool] = mapped_column(Boolean, nullable=True, default=True)
    immunizationScheduleId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("ImmunizationSchedule.id", use_alter=True, name="fk_immunizationrecord_immunizationschedule"), nullable=True)
    vaccinated_by : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id", use_alter=True, name="fk_immunizationrecord_vaccinatedby"), nullable=True)
    report_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Report.id", use_alter=True, name="fk_immunizationrecord_report", ondelete="CASCADE"), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    immunization : Mapped["ImmunizationSchedule"] = relationship(
        "ImmunizationSchedule", back_populates="mother_immunizations", foreign_keys=[immunizationScheduleId], lazy="selectin"
    )

    todoId : Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("ToDoInfo.id", use_alter=True), nullable=True)

    pregnancy : Mapped[Optional["Pregnancy"]] = relationship(
        "Pregnancy", back_populates="immunization_records", foreign_keys=[pregnancy_id], lazy="selectin"
    )

class MotherReportCheckList(Base):
    __tablename__ = "MotherReportCheckList"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    health_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id", use_alter=True, ), nullable=True)
    pregnancy_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Pregnancy.id", use_alter=True,), nullable=True)
    reportName : Mapped[str] = mapped_column(String, nullable=False)
    expected_date : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_date : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    type : Mapped[str] = mapped_column(String, nullable=True)
    required : Mapped[bool] = mapped_column(Boolean, nullable=True, default=True)
    immunizationScheduleId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("ImmunizationSchedule.id", use_alter=True, ), nullable=True)
    takenBy : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id", use_alter=True,), nullable=True)
    report_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Report.id", use_alter=True, ondelete="CASCADE"), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    todoId : Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("ToDoInfo.id", use_alter=True), nullable=True)

    pregnancy : Mapped[Optional["Pregnancy"]] = relationship(
        "Pregnancy", back_populates="mother_report_checklists", foreign_keys=[pregnancy_id], lazy="selectin"
    )
    

class BabyImmuizationRecord(Base):
    __tablename__ = "BabyImmunizationRecords"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    BirthRecordId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("BirthRecord.id", use_alter=True, name="fk_immunizationrecord_birthrecord"), nullable=True)
    vaccine_name : Mapped[str] = mapped_column(String, nullable=False)
    expected_date : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    required : Mapped[bool] = mapped_column(Boolean, nullable=True, default=True)
    vaccination_date : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    vaccinated_by : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id", use_alter=True, name="fk_immunizationrecord_vaccinatedby"), nullable=True)
    immunizationScheduleId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("ImmunizationSchedule.id", use_alter=True, name="fk_immunizationrecord_immunizationschedule"), nullable=True)
    report_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Report.id", use_alter=True, name="fk_immunizationrecord_report", ondelete="CASCADE"), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    todoId : Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("ToDoInfo.id", use_alter=True), nullable=True)


class ImmunizationSchedule(Base):
    __tablename__ = "ImmunizationSchedule"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vaccineName : Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    type : Mapped[str] = mapped_column(String, nullable=False)
    monthFrom : Mapped[int] = mapped_column(Integer, nullable=False)
    required : Mapped[bool] = mapped_column(Boolean, nullable=True)

    videoUrl : Mapped[str] = mapped_column(String, nullable=True)
    imageUrl : Mapped[str] = mapped_column(String, nullable=True)

    mother_immunizations : Mapped[List["MotherImmunizationRecord"]] = relationship(
        "MotherImmunizationRecord", back_populates="immunization", foreign_keys="MotherImmunizationRecord.immunizationScheduleId", lazy="selectin"
    )

    todoId : Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("ToDoInfo.id", use_alter=True), nullable=True)



class WeekWisePregnancyInfo(Base):
    __tablename__ = "WeekWisePregnancyInfo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    week : Mapped[int] = mapped_column(Integer, nullable=False)
    pregnancyTips : Mapped[str] = mapped_column(String, nullable=False)
    trimester : Mapped[str] = mapped_column(String, nullable=False)
    babySize : Mapped[str] = mapped_column(String, nullable=True)
    babyTransitionUrl : Mapped[str] = mapped_column(String, nullable=True)
    babyImageUrl : Mapped[str] = mapped_column(String, nullable=True)
    babyVideoUrl : Mapped[str] = mapped_column(String, nullable=True)
    whatsappTemplateId : Mapped[str] = mapped_column(String, nullable=True)
    emailTemplateId : Mapped[str] = mapped_column(String, nullable=True)

class ToDoInfo(Base):
    __tablename__ = "ToDoInfo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    week: Mapped[int] = mapped_column(Integer, nullable=True)
    day: Mapped[int] = mapped_column(Integer, nullable=True)
    month : Mapped[int] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    imageUrl : Mapped[str] = mapped_column(String, nullable=True)
    videoUrl : Mapped[str] = mapped_column(String, nullable=True)
    required : Mapped[bool] = mapped_column(Boolean, nullable=True, default=True)
    data : Mapped[dict] = mapped_column(JSONB, nullable=True)
    entityId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("entity.id", use_alter=True, name="fk_todoinfo_entity", ondelete="cascade"), nullable=True)
    deletedAt: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    contentTypeID: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("content_types.id", use_alter=True, name="fk_todoinfo_contenttype", ondelete="cascade"), nullable=True)

class BabyMilestones(Base):
    __tablename__ = "BabyMilestones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    birthRecordId: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("BirthRecord.id", use_alter=True, name="fk_weekbabymilestones_birthrecord", ondelete="cascade"), nullable=True)
    expected_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    milestone: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    achieved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    completed: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    todoId: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("ToDoInfo.id"), nullable=True)


class ReminderConfig(Base):

    __tablename__ = "ReminderConfig"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    remainder_type: Mapped[str] = mapped_column(String, nullable=False)
    userid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("User.id"), nullable=True)
    channels: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    frequency: Mapped[str] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    next_reminder_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_reminder_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    slug: Mapped[str] = mapped_column(String, nullable=True)

    configurable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    schedules : Mapped[List["ReminderSchedules"]] = relationship("ReminderSchedules", back_populates="reminder_config", cascade="all, delete-orphan")


    appointment_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Appointment.id", use_alter=True, name="fk_reminderconfig_appointment", ondelete="CASCADE"), nullable=True)
    pregnancy_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Pregnancy.id", use_alter=True, name="fk_reminderconfig_pregnancy", ondelete="CASCADE"), nullable=True)
    birth_record_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("BirthRecord.id", use_alter=True, name="fk_reminderconfig_birthrecord", ondelete="CASCADE"), nullable=True)
    prescription_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Prescription.id", use_alter=True, name="fk_reminderconfig_prescription", ondelete="CASCADE"), nullable=True)

class ReminderSchedules(Base):
    __tablename__ = "ReminderSchedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reminder_config_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ReminderConfig.id", ondelete="CASCADE"), nullable=False)
    schedule_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    reminder_config: Mapped["ReminderConfig"] = relationship("ReminderConfig", back_populates="schedules")


class KeyStore(Base):
    __tablename__ = "KeyStore"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    value: Mapped[str] = mapped_column(String, nullable=True)
    data : Mapped[dict] = mapped_column(JSONB, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class WhatsappBotMessages(Base):
    __tablename__ = "WhatsappBotMessages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class MedicalReading(Base):
    __tablename__ = "MedicalReading"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_name: Mapped[str] = mapped_column(String, nullable=True)
    value: Mapped[float] = mapped_column(Float, nullable=True)
    unit: Mapped[str] = mapped_column(String(20), nullable=True)
    riskStatus: Mapped[str] = mapped_column(String(20), nullable=True)
    riskCategory: Mapped[str] = mapped_column(String(20), nullable=True)

    reason: Mapped[str] = mapped_column(String, nullable=True)
    medical_term: Mapped[str] = mapped_column(String(50), nullable=True)

    typical_min_value: Mapped[str] = mapped_column(String, nullable=True)
    typical_max_value: Mapped[str] = mapped_column(String, nullable=True)

    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("Report.id"), nullable=True)
    health_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("HealthData.id"), nullable=False)
    
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())



   

class Blog(Base):
    __tablename__ = "Blog"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title : Mapped[str] = mapped_column(String)
    summery : Mapped[str] = mapped_column(String, nullable=True)
    route : Mapped[str] = mapped_column(String, unique=True, index=True)
    content : Mapped[str] = mapped_column(String)
    visible : Mapped[bool] = mapped_column(Boolean, default=True)
    headerImageurl : Mapped[str] = mapped_column(String, nullable=True)
    createdby : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id", use_alter=True, name="fk_content_creator"), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updatedAt : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category : Mapped[str] = mapped_column(String,default="common",nullable=True,index=True)

    users = relationship("User", foreign_keys=[createdby],lazy="selectin")

    # Relationship to BlogStats
    stats: Mapped[List["BlogStats"]] = relationship(
        "BlogStats",
        back_populates="blog",
        foreign_keys="BlogStats.blog_id",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


    viewCount : Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    likeCount : Mapped[int] = mapped_column(Integer,  default=0, nullable=True)
    shareCount : Mapped[int] = mapped_column(Integer, default=0 , nullable=True)
    commentCount : Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    actions: Mapped[list[dict]] = mapped_column(JSONB, nullable=True)

    tags: Mapped[List[str]] = mapped_column(ARRAY(String), default=list, nullable=True)




class BlogStats(Base):
    __tablename__ = "BlogStats"
    id: Mapped[int] = mapped_column(Integer,primary_key = True, autoincrement= True)
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("User.id"), nullable=False)
    blog_id : Mapped[int] = mapped_column(ForeignKey("Blog.id"), nullable=False)
    # optional reference to a Content record (many BlogStats rows may point to a content)
    type : Mapped[str] = mapped_column(String,index=True)
    comment : Mapped[str] = mapped_column(String, nullable=True)

    # relationships
    blog: Mapped["Blog"] = relationship(
        "Blog", back_populates="stats", foreign_keys=[blog_id], lazy="selectin"
    )

    createdAt = mapped_column(TIMESTAMP, server_default=func.now())


class SeoData(Base):
    __tablename__ = "SeoData"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    page_route: Mapped[str] = mapped_column(String, unique=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    keywords: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    canonical_url: Mapped[str] = mapped_column(String, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

# class LayoutMaster(Base):
#     __tablename__ = "layout_master"

#     id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     config_schema: Mapped[dict] = mapped_column(JSONB, nullable=False)
#     preview_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

#     # Relationship
#     layouts: Mapped[List["LandingPageLayout"]] = relationship("LandingPageLayout", back_populates="layout_master")


# class LandingPage(Base):
#     __tablename__ = "landing_page"

#     id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("entity.id"), nullable=False)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

#     entity: Mapped["Entity"] = relationship("Entity", back_populates="landing_pages")
#     layouts: Mapped[List["LandingPageLayout"]] = relationship("LandingPageLayout", back_populates="landing_page")


# class LandingPageLayout(Base):
#     __tablename__ = "landingpage_layout"

#     id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     landing_page_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("landing_page.id"), nullable=False)
#     layout_master_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("layout_master.id"), nullable=False)
#     order: Mapped[int] = mapped_column(Integer, nullable=False)
#     input_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
#     isVisible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
#     landing_page: Mapped["LandingPage"] = relationship("LandingPage", back_populates="layouts")
#     layout_master: Mapped["LayoutMaster"] = relationship("LayoutMaster", back_populates="layouts")

# class AppLogs(Base):
#     __tablename__ = "AppLogs"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     app_name : Mapped[str] = mapped_column(String, nullable=True)
#     log_type: Mapped[str] = mapped_column(String, nullable=False)
#     message: Mapped[str] = mapped_column(String, nullable=True)
#     data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
#     createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class KickCounter(Base):
    __tablename__ = "KickCounter"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pregnancy_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("Pregnancy.id", use_alter=True, name="fk_kickcounter_pregnancy"), nullable=True)
    count : Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    period : Mapped[str] = mapped_column(String, nullable=False)
    startTime : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    endTime : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class BreastFeedingRecord(Base):
    __tablename__ = "BreastFeedingRecord"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    birthRecordId : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("BirthRecord.id", use_alter=True, name="fk_feedingpattern_birthrecord"), nullable=True)
    duration : Mapped[Optional[str]] = mapped_column(String, nullable=True)
    feedingTime : Mapped[datetime] = mapped_column(DateTime, nullable=False)
    side : Mapped[Optional[str]] = mapped_column(String, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())    

class RAGKnowledge(Base):
    __tablename__ = "rag_knowledge"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    health_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    wellness_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    raw_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())