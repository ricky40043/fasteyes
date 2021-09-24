from fastapi import APIRouter, Depends, HTTPException
from app.api.routes import authentication, user, company, device, staff, deviceUuid, hardwareUuid, observation, \
    send_email

router = APIRouter()

router.include_router(authentication.router, tags=["authentication"])
router.include_router(user.router, tags=["user"])
router.include_router(company.router, tags=["Comapny"])
router.include_router(device.router, tags=["Device"])
router.include_router(staff.router, tags=["staff"])
router.include_router(deviceUuid.router, tags=["DeviceUuid"])
router.include_router(hardwareUuid.router, tags=["HardwareUuid"])
router.include_router(observation.router, tags=["Observation"])
# router.include_router(send_email.router, tags=["send_email"])
