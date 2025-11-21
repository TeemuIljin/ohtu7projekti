from repositories.ViiteRepository import ViiteRepository
from services.ViiteService import ViiteService
from ConsoleIO import ConsoleIO
from app import App


def main():
    user_repository = ViiteRepository()
    user_service = ViiteService(user_repository)
    console_io = ConsoleIO()
    app = App(user_service, console_io)

    app.run()


if __name__ == "__main__":
    main()
