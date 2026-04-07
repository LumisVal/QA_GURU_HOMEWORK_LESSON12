import allure
from selene import browser, have, command
from model.user import User


class RegistrationPage:

    @allure.step("Открыть страницу регистрации")
    def open(self):
        browser.open("/automation-practice-form")
        browser.driver.execute_script("$('#fixedban').remove()")
        browser.driver.execute_script("$('footer').remove()")
        return self

    @allure.step("Заполнить форму данными пользователя")
    def register(self, user: User):
        browser.element('#firstName').type(user.first_name)
        browser.element('#lastName').type(user.last_name)
        browser.element('#userEmail').type(user.email)
        browser.element(f'[name=gender][value="{user.gender}"]').perform(command.js.click)

        browser.element('#userNumber').type(user.phone)

        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__month-select').type(user.birth_month)
        browser.element('.react-datepicker__year-select').type(str(user.birth_year))
        browser.element(f'.react-datepicker__day--0{user.birth_day}:not(.react-datepicker__day--outside-month)').click()

        browser.element('#subjectsInput').type(user.subjects[0]).press_enter()
        browser.all('.custom-checkbox').element_by(have.exact_text(user.hobby)).click()

        browser.element('#uploadPicture').send_keys(user.picture)
        browser.element('#currentAddress').type(user.address)
        browser.element('#state').click()
        browser.all('#stateCity-wrapper div').element_by(have.exact_text(user.state)).click()
        browser.element('#city').click()
        browser.all('#stateCity-wrapper div').element_by(have.exact_text(user.city)).click()

        browser.element('#submit').perform(command.js.click)
        return self

    @allure.step("Проверить данные в таблице результата")
    def should_have_registered(self, user: User):
        browser.element('.table-responsive').all('td').should(
            have.texts(
                user.full_name,
                user.email,
                user.gender,
                user.phone,
                user.birth_date,
                user.subjects[0],
                user.hobby,
                user.picture_name,
                user.address,
                f'{user.state} {user.city}'
            )
        )
        return self