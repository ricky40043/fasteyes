# from cryptography.hazmat.primitives.hashes import MD5
# from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text
# from app.db.database import Base
# from datetime import datetime
#
#
# class face_feature(Base):
#     __tablename__ = "face_features"
#     id = Column(Integer, primary_key=True, index=True)
#     created_at = Column(DateTime, index=True)
#     updated_at = Column(DateTime, index=True)
#     raw_face_feature_uuid = Column(Text, index=True)
#     staff_id = Column(Integer, ForeignKey("staffs.id"))
#
#     def __init__(self, staff_id, raw_face_feature_uuid):
#         self.staff_id = staff_id
#         self.raw_face_feature = raw_face_feature_uuid
#         self.created_at = datetime.now()
#         self.updated_at = datetime.now()
