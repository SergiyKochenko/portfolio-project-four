- [**UX (User Experience)**](#ux-user-experience)
  - [**User Stories**](#user-stories)
- [**Design and Site Structure**](#design-structure)
  - [**Functional Structure**](#functional-structure)
  - [**Wireframes**](#wireframes)
- [**Features**](#features)
  - [**Responsive Design**](#responsive-design)
- [**Technologies**](#technologies)
  - [**Languages**](#languages)
  - [**Frameworks and Libraries**](#frameworks)
  - [**Tools**](#tools)
- [**Testing**](#testing)
- [**Deployment**](#deployment)
- [**Credits**](#credits)
  - [**Code**](#code)
  - [**Content**](#content)
  - [**Media**](#media)
  - [**Inspiration**](#inspiration)
  - [**Acknowledgments**](#acknowledgments)

 
# Portfolio Project 4 - Aquarium  
![](static/images/fish.jpg)

The deployed [AQUARIUM](https://app-portfolio-project-four.herokuapp.com/) app.

The [GitHub repository](https://sergiykoche-portfoliopr-sugfh0sfbwm.ws-eu90.gitpod.io/)

Project goals
This is the fourth project under the Code Institute Diploma in Software Development (E-commerce Applications) program. This website is a fictional aquariumistics called AQUARIUM. It is designed to be responsive and accessible on a variety of devices for the ease of use of the site by potential users.


## UX (User Experience)

### User stories

#### First time visitor goals

As a first time visitor, I want:
* to easily understand the main purpose of the site,
* to be able to easily navigate throughout the site,
* to be able to register a user account to access all content without restrictions,
* to be able to reserve a day and time for a service, view booking details and make changes to created bookings and delete my bookings,
* to be able to log out of my user account.
       
        
#### Returning and frequent user goals

As a returning user, I want:
* to sign in to my user account,
* to make a service booking, 
* to view my booking details, 
* to edit my booking details or delete them.
* to sign out of my account to keep my account safe.


#### Site Administrator goals
As a Site Administrator I would like to be able to create, view, edit and delete booking data.    

[Back to the top](#table-of-contents)


### Agile tools

The GitHub Projects section was used as a [Kanban board](https://github.com/users/SergiyKochenko/projects/6) for the development of this project, which made it possible to break down the project execution into subtasks and make it easier to complete and track project progress.
[User stories](https://github.com/SergiyKochenko/portfolio-project-four/issues) were used to break down the project into sub-tasks and placed on the Kanban board to work on them and track progress.


<!-- ---------------------------------- -->


## Design and Site structure

The site was based on the Blog template from the CodeInstitute site. The look of the site, color scheme, font, logo and image for the home page were made by myself from the template.
The main page layout can be seen below:

<details>
<summary>AqueriumHouse website design template </summary>

![Home page](static/assets/img/main-page.jpg)

</details>
<br />





<!-- ------------------------------------------ -->


### Functional Structure

**Home page:** The home page contains a menu, logo and an image that gives the user an idea of ​​the type of service provided. Under the logo in the center are links to register a new user or login for an existing user.
Registration and login are also available from the navigation bar.

**Registration page:** The user must create an account to make a reservation. !!!!!!!!!!!!!!!!!!!!!!!!!!!!
To do this, user is asked to fill out a form on the page with the required fields: username and password. There is also an optional email field.

**Login page:** A username and password are required to log in existing users.
The user can use the navigation menu or the link under the logo on the home page.
After a successful login, the user receives a message at the top of the screen and is redirected to the main page. !!!!!!!!!!!!!!!!!!!!!

**Logout page:** Logging out of the account is done through the menu, after which the user is redirected to the logout page where user must confirm his desire to log out of the account. After a successful logout, the user is returned to the main page and receives a message at the top of the screen.

**Booknow page:** The Booknow page is only available to authenticated users.
The user is asked to fill out a form with the required fields - name, service, time and date, and an optional field - phone, email.
After filling out the form, the user is redirected to the page of current bookings.

**Booking page:** Only authenticated users have access to the Booking page. The link to this page becomes visible in the navigation menu once a user is authenticated. Booking page shows to user information about made bookings and contains Change button and Delete button for manage booking.


**Change booking page:** This page is available only to authenticated users and has the same functionality and form as the Booknow page, where users can change  booking details.

**Delete booking page:** This page is only available to authenticated users and has the same functionality and form as the Booknow page, where the user can change the booking details. The user has the ability to delete user's booking by selecting the Delete button on the Booking page. After that, user will be redirected to the delete page where user needs to confirm user's intention. After successfully deleting the booking, user will return to the Booking page and and receives a message at the top of the screen.
Also, if the user changes user's mind, user can return to the page by clicking on the Back to my Bookings button.

[Back to the top](#table-of-contents)

MADE FORMATING HTML WITH: https://www.freeformatter.com/html-formatter.html#before-output