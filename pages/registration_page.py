from selene import browser, have, command



class RegistrationPage:

    def open(self):
        browser.open('https://demoqa.com/automation-practice-form')
        browser.driver.execute_script("document.querySelector('#fixedban')?.remove()")
        browser.driver.execute_script("document.querySelector('footer')?.remove()")
        return self

    def register(self, user):
        browser.element('#firstName').type(user.first_name)
        browser.element('#lastName').type(user.last_name)
        browser.element('#userEmail').type(user.email)

        browser.all('[name=gender]').element_by(have.value(user.gender)).element('..').click()

        browser.element('#userNumber').type(user.phone_number)

        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__month-select').type(user.birth_month)
        browser.element('.react-datepicker__year-select').type(str(user.birth_year))
        browser.element(
            f'.react-datepicker__day--0{user.birth_day}:not(.react-datepicker__day--outside-month)'
        ).click()

        browser.element('#subjectsInput').type(user.subject).press_enter()
        browser.all('label[for^="hobbies-checkbox"]').element_by(have.exact_text(user.hobby)).click()
        browser.element('#currentAddress').type(user.address)

        browser.element('#state').perform(command.js.scroll_into_view)
        browser.element('#state').click()
        browser.element('#react-select-3-input').type(user.state).press_enter()

        browser.element('#city').click()
        browser.element('#react-select-4-input').type(user.city).press_enter()

        browser.element('#submit').perform(command.js.click)
        return self

    def should_have_registered(self, user):
        table = browser.element('.table-responsive')

        table.element('//td[text()="Student Name"]/following-sibling::td').should(
            have.exact_text(f'{user.first_name} {user.last_name}')
        )
        table.element('//td[text()="Student Email"]/following-sibling::td').should(
            have.exact_text(user.email)
        )
        table.element('//td[text()="Gender"]/following-sibling::td').should(
            have.exact_text(user.gender)
        )
        table.element('//td[text()="Mobile"]/following-sibling::td').should(
            have.exact_text(user.phone_number)
        )
        table.element('//td[text()="Date of Birth"]/following-sibling::td').should(
            have.exact_text(f'{user.birth_day} {user.birth_month},{user.birth_year}')
        )
        table.element('//td[text()="Subjects"]/following-sibling::td').should(
            have.exact_text(user.subject)
        )
        table.element('//td[text()="Hobbies"]/following-sibling::td').should(
            have.exact_text(user.hobby)
        )
        table.element('//td[text()="Address"]/following-sibling::td').should(
            have.exact_text(user.address)
        )
        table.element('//td[text()="State and City"]/following-sibling::td').should(
            have.exact_text(f'{user.state} {user.city}')
        )
