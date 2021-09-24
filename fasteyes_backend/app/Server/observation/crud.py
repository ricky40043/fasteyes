from datetime import datetime
from sqlalchemy.orm import Session

from app.core.config import default_staff
from app.models.domain.Device import device
from app.models.domain.Error_handler import UnicornException
from app.models.domain.Observation import observation
from app.models.domain.Staff import staff
from app.models.domain.user import user
from app.models.schemas.Observation import ObservationPostViewModel, ObservationPatchViewModel


def get_default_staff_id(db: Session):
    return db.query(staff).filter(staff.serial_number == default_staff).first()


def create_observation(db: Session, observation_in: ObservationPostViewModel, device_id: int):
    db.begin()
    try:
        if observation_in.staff_id == -1:
            observation_in.staff_id = get_default_staff_id(db).id

        observation_db = observation(**observation_in.__dict__, device_id=device_id)
        db.add(observation_db)
        db.commit()
        db.refresh(observation_db)
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=create_observation.__name__, description=str(e), status_code=500)
    return observation_db


def delete_observation_by_device_id(db: Session, device_id: int):
    db.begin()
    try:
        db.query(observation).filter(observation.device_id == device_id).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=delete_observation_by_device_id.__name__, description=str(e), status_code=500)
    return "Delete observation by device_id Done"


def get_Observations_by_device_id_and_timespan(db: Session, staff_id: int, start_timestamp: datetime,
                                               end_timestamp: datetime):
    # test
    start_timestamp = start_timestamp
    end_timestamp = end_timestamp
    return db.query(observation).filter(observation.staff_id == staff_id).filter(
        observation.updated_at >= start_timestamp, observation.updated_at <= end_timestamp).all()


def get_all_observations_by_device_id(db: Session, device_id: int):
    return db.query(observation).filter(observation.device_id == device_id).all()


def update_observation(db: Session, observation_id: int, obsPatch: ObservationPatchViewModel):
    db.begin()
    try:
        observation_db = db.query(observation).filter(observation.id == observation_id).first()
        observation_db.staff_id = obsPatch.staff_id
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=update_observation.__name__, description=str(e), status_code=500)
    return observation_db


def get_observation_by_id(db: Session, observation_id: int):
    return db.query(observation).filter(observation.id == observation_id).first()


def get_Observations_by_device_id_and_staff_id(db: Session, device_id: int, staff_id: int):
    return db.query(observation).filter(observation.device_id == device_id, observation.staff_id == staff_id).all()


def get_Observations_by_staff_id(db: Session, staff_id: int):
    return db.query(observation).filter(observation.staff_id == staff_id).all()


def delete_observation_by_id(db: Session, observation_id: int):
    db.begin()
    try:
        observation_db = db.query(observation).filter(observation.id == observation_id).first()
        db.delete(observation_db)
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=update_observation.__name__, description=str(e), status_code=500)
    return observation_db


def delete_all_observation_by_device_id(db: Session, device_id: int):
    db.begin()
    try:
        observation_db = db.query(observation).filter(observation.device_id == device_id).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=update_observation.__name__, description=str(e), status_code=500)
    return observation_db


def delete_all_observation(db: Session):
    db.begin()
    try:
        observation_db = db.query(observation).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(str(e))
        raise UnicornException(name=update_observation.__name__, description=str(e), status_code=500)
    return observation_db


def check_observation_ownwer(db: Session, observation_id: int, user_id: int):
    observation_db = db.query(observation).filter(observation.id == observation_id).first()
    Device_db = db.query(device).filter(device.id == observation_db.device_id).first()
    return db.query(user).filter(user.id == Device_db.user_id).first()
