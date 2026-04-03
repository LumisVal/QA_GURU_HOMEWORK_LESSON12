from data.users import student
from pages.registration_page import RegistrationPage


registration_page = RegistrationPage()


def test_student_registration():
    registration_page.open()
    registration_page.register(student)
    registration_page.should_have_registered(student)
