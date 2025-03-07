from user_controller import router as user_router


def register_routers(app):
    # Register Blueprints here
    app.include_router(user_router)
