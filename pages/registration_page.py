import os
import allure
from selene import browser, have, command
from model.user import User


class RegistrationPage:

    @allure.step("Открыть страницу регистрации")
    def open(self):
        browser.open("/automation-practice-form")
        browser.driver.execute_script("document.querySelector('#fixedban')?.remove()")
        browser.driver.execute_script("document.querySelector('footer')?.remove()")
        return self

    @allure.step("Заполнить форму данными пользователя")
    def register(self, user: User):
        browser.element('#firstName').type(user.first_name)
        browser.element('#lastName').type(user.last_name)
        browser.element('#userEmail').type(user.email)
        browser.element(f'[name=gender][value="{user.gender}"]').perform(command.js.click)

        browser.element('#userNumber').type(user.phone_number)

        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__month-select').type(user.birth_month)
        browser.element('.react-datepicker__year-select').type(str(user.birth_year))
        browser.element(
            f'.react-datepicker__day--0{user.birth_day}:not(.react-datepicker__day--outside-month)'
        ).click()

        browser.element('#subjectsInput').type(user.subject).press_enter()
        if user.hobby == 'Sports':
            browser.element('label[for="hobbies-checkbox-1"]').click()
        elif user.hobby == 'Reading':
            browser.element('label[for="hobbies-checkbox-2"]').click()
        elif user.hobby == 'Music':
            browser.element('label[for="hobbies-checkbox-3"]').click()

        browser.element('#uploadPicture').send_keys(
            os.path.abspath(f'resources/{user.picture}')
        )
        browser.element('#currentAddress').type(user.address)

        browser.element('#state').click()
        browser.element('#react-select-3-input').type(user.state).press_enter()

        browser.element('#city').click()
        browser.element('#react-select-4-input').type(user.city).press_enter()

        browser.element('#submit').perform(command.js.click)
        return self

    @allure.step("Проверить данные в таблице результата")
    def should_have_registered(self, user: User):
        browser.element('.table-responsive').all('tbody tr td:last-child').should(
            have.texts(
                f'{user.first_name} {user.last_name}',
                user.email,
                user.gender,
                user.phone_number,
                f'{user.birth_day} {user.birth_month},{user.birth_year}',
                user.subject,
                user.hobby,
                user.picture,
                user.address,
                f'{user.state} {user.city}'
            )
        )
        return self