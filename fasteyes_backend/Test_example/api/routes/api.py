from fastapi import APIRouter, Depends, HTTPException

from Test.api.routes import user

from Test.api.routes.user import test_add_user

router = APIRouter()

router.include_router(user.router, tags=["user"])
# router.include_router(authentication.router, tags=["test_authentication"], prefix="/test_user")
# router.include_router(products.router, tags=["test_products"], prefix="/products")
# router.include_router(tags.router, tags=["test_tags"], prefix="/tags")
#
# router.include_router(borrow.router, tags=["test_borrow"])
# from Test.api.routes.authentication import test_register, test_get_my_products, test_get_user_id_products, test_get_Users, \
#     test_user_me_fail, test_login_token_and_user_me
#
# from Test.api.routes.products import test_get_products,test_create_products

