# ***Lottonero - Portfolio Project 5***
---
# **1. Key project information**

- **Description :** This Portfolio Project 5 website called **Lottonero** is a site that provides detailed **statistical** analysis, trend insights, and **predictive** outcomes based on comprehensive data modeling. The feature of Lottonero are designed to enhance the user's understanding of the game's intricacies, empowering them to make better **informed decisions** when choosing the numbers of their EuroMillions lotto ticket. Lottonero is a **subscription** base e-commerce platform that allows the user to choose between two main features, **AI Predictions** and **Lotto Statistics**. Whereby, on one hand, AI Predictions provides a series of **predicted lotto tickets** consisting of predictions based on **Patterns** or **Combinations** and on the other hand, the Statistics feature provides three pages of analytical data based on the EuroMillions jackpot history.
- **Key project goal :** To offer all visitors of **Lottonero** site access to data modelling that enhances playing strategies.
- **Audience :** Despite being affiliated to the EuroMillions lottery, there are no age limitations. Hence, the website does not market or encourage gambling but rather provides an informative entertainment platform. The main audience of this website include individuals with personal interest in the EuroMillions Lottery.
- **Live version :** Live version of **Lottonero** can be viewed at [https://lottonero-e7dc9a7038d2.herokuapp.com/](https://lottonero-e7dc9a7038d2.herokuapp.com/).
- **Dummy Card :** 4242 4242 4242 4242, expiry 05/27, cvc 123 
- **Developer :** [Jalal Semaan](https://github.com/jjsemaan/lottonero)

![Mockup](/docs/mockup.JPG)

# **2. Table of Contents**

- [**1. Key project information**](https://github.com/jjsemaan/lottonero/blob/main/README.md#1-key-project-information)
- [**2. Table of Contents**](https://github.com/jjsemaan/lottonero/blob/main/README.md#2-table-of-contents)
- [**3. User Experience (UX)**](https://github.com/jjsemaan/lottonero/blob/main/README.md#3-user-experience-ux)
  * [**3.1. The Strategy Plane**](https://github.com/jjsemaan/lottonero/blob/main/README.md#31-the-strategy-plane)
    + [**3.1.1 The Idea**](https://github.com/jjsemaan/lottonero/blob/main/README.md#311-the-idea)
    + [**3.1.2 The Ideal User**](https://github.com/jjsemaan/lottonero/blob/main/README.md#312-the-ideal-user)
    + [**3.1.3 Site Goals**](https://github.com/jjsemaan/lottonero/blob/main/README.md#313-site-goals)
    + [**3.1.4 Epics**](https://github.com/jjsemaan/lottonero/blob/main/README.md#314-epics)
    + [**3.1.5 User stories**](https://github.com/jjsemaan/lottonero/blob/main/README.md#315-user-stories)
  * [**3.2. The Scope Plane**](https://github.com/jjsemaan/lottonero/blob/main/README.md#32-the-scope-plane)
    + [**3.2.1. Features to be implemented**](https://github.com/jjsemaan/lottonero/blob/main/README.md#321-features-to-be-implemented)
  * [**3.3. The Structure Plane**](https://github.com/jjsemaan/lottonero/blob/main/README.md#33-the-structure-plane)
    + [**3.3.1. Site Maps**](https://github.com/jjsemaan/lottonero/blob/main/README.md#331-site-maps)
    + [**3.3.2. Database Schemas**](https://github.com/jjsemaan/lottonero/blob/main/README.md#332-database-schemas)
  * [**3.4. Wire-frames**](https://github.com/jjsemaan/lottonero/blob/main/README.md#34-wire-frames)
  * [**3.5. The Surface Plane**](https://github.com/jjsemaan/lottonero/blob/main/README.md#35-the-surface-plane)
    + [**3.5.1. Logo**](https://github.com/jjsemaan/lottonero/blob/main/README.md#351-logo)
    + [**3.5.2. Color pallette**](https://github.com/jjsemaan/lottonero/blob/main/README.md#352-color-pallette)
    + [**3.5.3. Fonts**](https://github.com/jjsemaan/lottonero/blob/main/README.md#353-fonts)
    + [**3.5.4. Icons and pictures**](https://github.com/jjsemaan/lottonero/blob/main/README.md#354-icons-and-pictures)
- [**4. Features**](https://github.com/jjsemaan/lottonero/blob/main/README.md#4-features)
  * [**4.1. Features used in every HTML template**](https://github.com/jjsemaan/lottonero/blob/main/README.md#41-features-used-in-every-html-template)
    + [**4.1.1 Header**](https://github.com/jjsemaan/lottonero/blob/main/README.md#411-header)
    + [**4.1.2. Footer**](https://github.com/jjsemaan/lottonero/blob/main/README.md#412-footer)
    + [**4.1.3. Favicon**](https://github.com/jjsemaan/lottonero/blob/main/README.md#413-favicon)
    + [**4.1.4. Error Pages**](https://github.com/jjsemaan/lottonero/blob/main/README.md#414-error-pages)
    + [**4.1.5. Toasts**](https://github.com/jjsemaan/lottonero/blob/main/README.md#415-toasts)
  * [**4.2. Main Content**](https://github.com/jjsemaan/lottonero/blob/main/README.md#42-main-content)
    + [**4.2.1. Landing Page**](https://github.com/jjsemaan/lottonero/blob/main/README.md#421-landing-page)
    + [**4.2.2. Subscriptions Page**](https://github.com/jjsemaan/lottonero/blob/main/README.md#422-subscriptions-page)
    + [**4.2.3. AI Predictions Pages**](https://github.com/jjsemaan/lottonero/blob/main/README.md#423-ai-predictons-pages)
    + [**4.2.4. Statistics Pages**](https://github.com/jjsemaan/lottonero/blob/main/README.md#424-statistics-pages)
    + [**4.2.5. Alltime Hits Pages**](https://github.com/jjsemaan/lottonero/blob/main/README.md#425-alltime-hits-pages)
    + [**4.2.6. About Page**](https://github.com/jjsemaan/lottonero/blob/main/README.md#426-about-page)
    + [**4.2.7. Contact Page**](https://github.com/jjsemaan/lottonero/blob/main/README.md#427-contact-page)
    + [**4.2.8. Backoffice Page**](https://github.com/jjsemaan/lottonero/blob/main/README.md#428-backoffice-page)
    + [**4.2.9. My Profile Page**](https://github.com/jjsemaan/lottonero/blob/main/README.md#429-my-profile-page)
    + [**4.2.10. Forms**](https://github.com/jjsemaan/lottonero/blob/main/README.md#4210-forms)
    + [**4.2.11. User Emails**](https://github.com/jjsemaan/lottonero/blob/main/README.md#4211-user-emails)
  * [**4.3. Future Features**](https://github.com/jjsemaan/lottonero/blob/main/README.md#43-future-features)
- [**5. Marketing**](https://github.com/jjsemaan/lottonero/blob/main/README.md#5-marketing)
  * [**5.1. Social Media Presence**](https://github.com/jjsemaan/lottonero/blob/main/README.md#51-social-media-presence)
  * [**5.2. Search Engine Optimization (SEO)**](https://github.com/jjsemaan/lottonero/blob/main/README.md#52-search-engine-optimization-seo)
- [**6. Validation, Testing & Bugs**](https://github.com/jjsemaan/lottonero/blob/main/README.md#6-validation-testing--bugs)
  * [**6.1. Validation**](https://github.com/jjsemaan/lottonero/blob/main/README.md#61-validation)
  * [**6.2. Testing**](https://github.com/jjsemaan/lottonero/blob/main/README.md#62-testing)
  * [**6.3. Bugs**](https://github.com/jjsemaan/lottonero/blob/main/README.md#63-bugs)
- [**7. Deployment**](https://github.com/jjsemaan/lottonero/blob/main/README.md#7-deployment)
  * [**7.1. Transfer of progress from IDE**](https://github.com/jjsemaan/lottonero/blob/main/README.md#71-transfer-of-progress-from-ide)
  * [**7.2. Offline cloning**](https://github.com/jjsemaan/lottonero/blob/main/README.md#72-offline-cloning)
  * [**7.3. Deployment Prerequisites**](https://github.com/jjsemaan/lottonero/blob/main/README.md#73-deployment-prerequisites)
    + [**7.3.1. Microsoft O365**](https://github.com/jjsemaan/lottonero/blob/main/README.md#731-email)
    + [**7.3.2. Retool DB**](https://github.com/jjsemaan/lottonero/blob/main/README.md#732-neon-tech-db)
    + [**7.3.3. Cloudinary Service**](https://github.com/jjsemaan/lottonero/blob/main/README.md#733-aws-cloud-service)
    + [**7.3.4. Stripe Configuration & Connection**](https://github.com/jjsemaan/lottonero/blob/main/README.md#734-stripe-configuration--connection)
    + [**7.3.5. Settings.py & file-tree**](https://github.com/jjsemaan/lottonero/blob/main/README.md#--735-settingspy---file-tree--)
  * [**7.4. Deployment to Heroku**](https://github.com/jjsemaan/lottonero/blob/main/README.md#74-deployment-to-heroku)
- [**8. Technologies & Credits**](https://github.com/jjsemaan/lottonero/blob/main/README.md#8-technologies---credits)
  * [**8.1. Technologies used to develop and deploy this project**](https://github.com/jjsemaan/lottonero/blob/main/README.md#81-technologies-used-to-develop-and-deploy-this-project)
  * [**8.2. Requirements.txt**](https://github.com/jjsemaan/lottonero/blob/main/README.md#82-requirementstxt)
  * [**8.3. Credits**](https://github.com/jjsemaan/lottonero/blob/main/README.md#83-credits)

---

# **3. User Experience (UX)**

## **3.1. The Strategy Plane**

### **3.1.1 The Idea**
- The intention of **lottonero** site is to be a friendly online platform where users can browse variaty playing startegies from two main categories, **AI Predictions** and **Statistics**. Almost all data information in lottonero is presented using visuals of ball images and graphs to maximise user engagement and to enhance UX/UI of the website.

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---
### **3.1.2 The Ideal User**

The target audience are individuals or groups with personal interest in the EuroMillios Lottery seeking inspiration and understanding on how jackpot randomisation works. 

- Ideal user likes EuroMillions
- Ideal user seeking credible predictice sources
- Ideal user seeking credible statistics

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---
### **3.1.3 Site Goals**

- Offer users ability understand EuroMillions trends
- Offer users ability to find predictions to play externally

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---
### **3.1.4 Epics**

As a thought process of the strategy plane, 30 issues were created and utilised. Please see below the detail list of issues with links, or a link to the project's [Kanban Board](https://github.com/users/jjsemaan/projects/9/views/1)



![Kanban Board](/docs/kanban.JPG)

- EPIC 1 : Create base html - [issue #1](https://github.com/jjsemaan/lottonero/issues/1)
- EPIC 2 : Create static resources - [issue #2](https://github.com/jjsemaan/lottonero/issues/2)
- EPIC 3 : Setup core dependencies - [issue #3](https://github.com/jjsemaan/lottonero/issues/3)
- EPIC 4 : Create footer - [issue #4](https://github.com/jjsemaan/lottonero/issues/4)
- EPIC 5 : Create navbar - [issue #5](https://github.com/jjsemaan/lottonero/issues/5)
- EPIC 6 : Add background image - [issue #6](https://github.com/jjsemaan/lottonero/issues/6)
- EPIC 7 : Create 404 page - [issue #7](https://github.com/jjsemaan/lottonero/issues/7)
- EPIC 8 : Create 500 page - [issue #8](https://github.com/jjsemaan/lottonero/issues/8)
- EPIC 9 : Create 403 page - [issue #9](https://github.com/jjsemaan/lottonero/issues/9)
- EPIC 10 : Create home page - [issue #10](https://github.com/jjsemaan/lottonero/issues/10)
- EPIC 12 : Scrape euromillions results - [issue #12](https://github.com/jjsemaan/lottonero/issues/12)
- EPIC 13 : Develop AI prediction model - [issue #13](https://github.com/jjsemaan/lottonero/issues/13)
- EPIC 14 : Add allauth - [issue #14](https://github.com/jjsemaan/lottonero/issues/14)
- EPIC 15 : Verify emails - [issue #15](https://github.com/jjsemaan/lottonero/issues/15)
- EPIC 16 : Style allauth forms - [issue #16](https://github.com/jjsemaan/lottonero/issues/16)
- EPIC 17 : Add UI staff functionality - [issue #17](https://github.com/jjsemaan/lottonero/issues/17)
- EPIC 18 : Create backoffice page - [issue #18](https://github.com/jjsemaan/lottonero/issues/18)
- EPIC 20 : Create statistics pages - [issue #20](https://github.com/jjsemaan/lottonero/issues/20)
- EPIC 21 : Create statistics models - [issue #21](https://github.com/jjsemaan/lottonero/issues/21)
- EPIC 23 : Create subscription model - [issue #23](https://github.com/jjsemaan/lottonero/issues/23)
- EPIC 24 : Create profile page - [issue #24](https://github.com/jjsemaan/lottonero/issues/24)
- EPIC 25 : Create subscription page - [issue #25](https://github.com/jjsemaan/lottonero/issues/25)
- EPIC 26 : Set up whitenoise - [issue #26](https://github.com/jjsemaan/lottonero/issues/26)
- EPIC 27 : Deploy to Heroku - [issue #27](https://github.com/jjsemaan/lottonero/issues/27)
- EPIC 30 : Create contact page and Newsletter - [issue #30](https://github.com/jjsemaan/lottonero/issues/30)
- EPIC 31 : Create about page - [issue #31](https://github.com/jjsemaan/lottonero/issues/31)
- EPIC 32 : Create Payment Gateway - [issue #32](https://github.com/jjsemaan/lottonero/issues/32)
- EPIC 33 : Create terms and conditions page - [issue #33](https://github.com/jjsemaan/lottonero/issues/33)
- EPIC 34 : Create Favicon - [issue #33](https://github.com/jjsemaan/lottonero/issues/34)
- EPIC 35 : Testing - [issue #35](https://github.com/jjsemaan/lottonero/issues/35)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **3.1.5 User stories**
User stories were created as Issues. Each user story uses the MoSCoW prioritization technique.
Each user story on the Kanban Board was given 2 labels (MoSCoW and Story Points) and a milestone.

MoSCoW prioritization technique stands for:
Must-Have: Critical requirements that must be implemented for the project to be considered successful.
Should-Have: Important requirements that are not critical but add significant value.
Could-Haves: Desirable features that would be nice to have but are not crucial.
Won't-Have: Features that are explicitly excluded from the project scope.

The **PERCENTAGE** of MoSCow from all Issues.
- **Must-Have** :   14 story points   ( 45 % )
- **Should-Have** : 10 story points   ( 32 % )
- **Could-Have** :  5 story points    ( 16 % )
- **Wont-Have** :   2 story points    ( 7 % )

---

## **3.2. The Scope Plane**

After deciding on the strategy (refer to below strategy diagram), the scope plane was carefully created.

![Lottonero Strategy](/docs/strategy.JPG)

### **3.2.1. Features**

- **Authentication** : Users can Register, access **My Profile** page where users can manage their information and preferences and cancel their subscriptions (CRUD)

- **Home** : Users can browse through the hamepage to check the latest EuroMillions Jackpot results and review winning predictions.

- **Orders** : Users can browse through the subscription options that are offered on monthly or annual basis.

- **Payment Gateway** : Payments for subscriptions are received securely via Stripe then the users are redirected back to the website.

- **Predictions** : Subscribers get access to two prediction models in separate pages, **AI Patterns** and **Combinations**, each offering over 30 predictions to choose from for the upcoming draw.

- **Lottery Statistics** : Subscribers get access to three statistical views in three separate pages, **Frequencies**, **Correlations** and **Combinations** offering visual analytics from EuroMillions jackpot history.

- **Scraping** : This feature offers seamless updates when run by the admins as it updates the homepage with the latest jackpot results scraped from the **Accessible Results** https://www.lottery.ie/accessible-results page of the EuroMillions website.

- **User Profile** : Page where users can manage all aspects of their account including changing names, emails, password and subscription cancellation.

- **Notifications** : Toasts and Email notifications are fully enabled for this website.


[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **3.3. The Structure Plane**

### **3.3.1. Site Maps**

The following site-maps show how the site is structured to **Logged in user** *( Appendix 1 )* ,**Not logged in user** *( Appendix 2 )* and **Site Admin** *( Appendix 3 )*.

*Appendix 1 - Site Map - Logged In*

![Site Map - Logged In](/docs/sitemap-loggedin.jpg)

*Appendix 2 - Site Map - Not Logged Out*

![Site Map - Not Logged Out](/docs/sitemap-loggedout.jpg)

*Appendix 3 - Site Map - Site Admin*

![Site Map - Logged In](/docs/sitemap-admin.jpg)

*Appendix 4 - Site Map - Logged In Subscriber Predictions*

![Site Map - Logged In](/docs/sitemap-subscriber-predictions.jpg)

*Appendix 5 - Site Map - Logged In Subscriber Statistics*

![Site Map - Logged In](/docs/sitemap-subscriber-statistics.jpg)

*Appendix 6 - Site Map - Logged In Subscriber Premium*

![Site Map - Logged In](/docs/sitemap-subscriber-premium.jpg)


[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **3.3.2. Database Schema**

The following schema presents the intended database structure *( Appendix 7 )* generated by pgAdmin software *( Appendix 7 )*.
N.B. The extended complete schema is exteremely large *( Appendix 8 )* due to the synchronisation with dj-stripe db. 
However, the main reason behind the synchronisation is to created a direct connection to Stripe as a future enhancement.

*Appendix 7 - Lottonero Schema*

![pgAdmin - Lottonero Schema](/docs/pg-schema.jpg)

*Appendix 8 - Complete Schema including dj-stripe*

![pgAdmin - Complete Schema](/docs/complete-schema.jpg)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **3.4. Wire-frames**

- **Header and Footer** : Header and footer is established on every single page. **Header** is displayed on top of each page, **Footer** is displayed at the very bottom of each page so it doesn't cover any content *( Appendix 9 )*. The footer constitutes Social Media Icons, a Newsletter section and copyright info.

*Appendix 9 - Header and Footer Wireframe*

![Header and Footer Wireframe](/docs/wireframes/header-footer-wireframe.JPG)

- **Landing page** : Provides the user with a clear understanding about the page. The page displays the latest EuroMillions jackpot details, the latest winning predictions, a button that opens a card providing futher additional info about the website, and an option for the user to subscribe for **Lottonero** services *( Appendix 10 )*.

*Appendix 10 - Landing Page Wireframe*

![Landing Page Wireframe](/docs/wireframes/landing-wireframe.JPG)

- **AI Patterns page** : Provides the user with a set of AI generated pattern-based predictions targeting the upcoming EuroMillions jackpot. 
Users are required to subscribe for this service otherwise access will be denied. *( Appendix 11 )*.

*Appendix 11 - AI Patterns Page Wireframe*

![AI Patterns Page Wireframe](/docs/wireframes/patterns-wireframe.JPG)

- **AI Combinations page** : Provides the user with a set of AI generated combination-based predictions targeting the upcoming EuroMillions jackpot. 
Users are required to subscribe for this service otherwise access will be denied. *( Appendix 12 )*.

*Appendix 12 - AI Combinations Page Wireframe*

![AI Combinations Page Wireframe](/docs/wireframes/combinations-wireframe.JPG)

- **Statistics Frequency page** : Provides the user with two advance statictical frequency charts presenting highest ranking / winning ball numbers as well as median and KDE curves. Users are required to subscribe for this service otherwise access will be denied. *( Appendix 13 )*.

*Appendix 13 - Statistics Frequency Page Wireframe*

![Statistics Frequency Page Wireframe](/docs/wireframes/stats-freq-wireframe.JPG)

- **Statistics Combinations page** : Provides the user with a statictical combinations graph presenting ball combinations from the jackpot history. Users are required to subscribe for this service otherwise access will be denied. *( Appendix 14 )*.

*Appendix 14 - Statistics Combinations Page Wireframe*

![Statistics Combinations Page Wireframe](/docs/wireframes/stats-combi-wireframe.JPG)

- **Statistics Correlations page** : Provides the user with a statictical correlations heatmap presenting ball correlations from the jackpot history. Users are required to subscribe for this service otherwise access will be denied. *( Appendix 15 )*.

*Appendix 15 - Statistics Correlations Page Wireframe*

![Statistics Correlations Page Wireframe](/docs/wireframes/stats-corr-wireframe.JPG)

- **Alltime Patterns page** : Provides the user with a list of the last 25 winning predictions from AI Patterns. *( Appendix 16 )*.

*Appendix 16 - Alltime Patterns Page Wireframe*

![Alltime Patterns Page Wireframe](/docs/wireframes/alltime-patterns-wireframe.JPG)

- **Alltime Combinations page** : Provides the user with a list of the last 25 winning predictions from AI Combinations. *( Appendix 17 )*.

*Appendix 17 - Alltime Combinations Page Wireframe*

![Alltime Combinations Page Wireframe](/docs/wireframes/alltime-combi-wireframe.JPG)

- **About page** : Provides the user with information about the website *( Appendix 18 )*.

*Appendix 18 - About Page Wireframe*

![About Page Wireframe](/docs/wireframes/about-wireframe.JPG)

- **Contact page** : Displays a contact form for the user to send a message to the website admin. If the user is logged in their email will be picked up automatically otherwise if the user is logged out, they will be prompted to add their email before sending *( Appendix 19 )*.

*Appendix 19 - Contact Page Wireframe*

![Contact Page Wireframe](/docs/wireframes/contact-wireframe.JPG)

- **Admin Backoffice page** : The Backoffice button appears only to logged-in andmins. Once clicked, it displays a list with three command buttons with use-instructions *( Appendix 20 )*.

*Appendix 20 - Admin Backoffice Page Wireframe*

![Admin Backoffice Page Wireframe](/docs/wireframes/admin-wireframe.JPG)

- **Profile page** : This is a user-profile management page where a user is able to make changes to their profile and view or cancel their subscriptions *( Appendix 21 )*.

*Appendix 21 - Profile Page Wireframe*

![Profile Page Wireframe](/docs/wireframes/profile-wireframe.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **3.5. The Surface Plane**

Once the Strategy, Scope, Structure and Skeleton Planes were realised, the Surface Plane (Design) is developed.

### **3.5.1. Logo**

The Logo was written using Google font futura in an attemp to blend with the remaining contents on the site. A designer logo may be added later as a future enhancement *( Appendix 22 )*

*Appendix 22 - Logo*

![Logo](/docs/logo.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **3.5.2. Color pallette**

Based on the website name Lottonero with 'nero' meaning black, the website is mainly based on black and Grey text over a white background with a variation on cheerful colors inspired by the standard bootstrap buttons that matched the main Lottonero background image and referenced using the [Color-Hex Website](https://www.color-hex.com/color-palette/24304). *( Appendix 23 )*

*Appendix 23 - Color pallette*

![Color pallette](/docs/color-pallette.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **3.5.3. Fonts**

[Adobe Fonts](https://fonts.adobe.com/fonts/futura-pt) site was used to pick the best typography style to match the theme. 
As a developer I needed to ensure that all text is clearly displayed and comprehended

One font was picked and saved in base.css:
 - futura-pt (Sans Serif) -  *( Appendix 24 )*

*Appendix 24 - Futura-pt Font*

![Futura-pt Font](/docs/futura-font.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **3.5.4. Icons and pictures**

Icons used throughout the projects are [Font Awesone Icons](https://fontawesome.com/). 
The Font Awesome icons were mainly used for the Account (user profile), log out as well as social media functionality as buttons in the top nave and the footer respectively to better enhance user experience.

Graphic designer Elie Obeid from [ParaBIM Ltd.](https://parabim.ie/) in Ireland (CRO registration 699503 - founded by Lottonero's developer Jalal Semaan) had provided the main background image used in this project.

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

# **4. Features**

## **4.1. Features used in every HTML template**

### **4.1.1 Header**
- A Mobile Top Header containing a Logo in the top left, which is also used as a link to the Home page `{% url 'home' %}`. The logo disappears when the hamburger menu appears when the resolution changes to less than 992 pixels in width. User **Account** and **Log Out** icons are in the top right corner and will remain there on smaller screens, when the resolution changes to less than 992 pixels in width. *( Appendix 25 )*
- A Main Nav subheader contains all Lottonero pages. This will allow the user to navigate through the pages and to navigate back to home page when click on logo. *( Appendix 26 )*
- Both '{% include 'includes/mobile-top-header.html' %}' and '{% include 'includes/main-nav.html' %}' are included in `base.html`.

*Appendix 25 - Header on Larger Screens*

![Header on Larger Screens](/docs/features/header-desktop.JPG)

*Appendix 26 - Header on devices less 992px in width*

![Header on devices less 992px](/docs/features/header-mobile.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.1.2. Footer**

- Footer  *( Appendix 27 )* is designed to reveal basic social media icons for **Lottonero**, the integrated [Mailchimp Newsletter](https://mailchimp.com/landers/newsletters/) and Copyright credentials.
- Footer is designed to cover full width `width: 100%` of the browsing window.
- Footer is responsive and remains unchanged on smaller screens below 992 pixels in width.
- Footer is included in `base.html`.

*Appendix 27 - Footer*

![Footer](/docs/features/footer.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.1.3. Favicon**

- Every template in this project is equipped with a Favicon. This is useful when multiple tabs are opened. *( Appendix 28)*

*Appendix 28 - Favicon*

![Favicon](/static/favicon.ico)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.1.4. Error Pages**

- This project is developed to include custom error pages. In case the user clicks on a broken link, submits an action that isn't supported or tries to reach a certain page without permission, then the user isn't completely "cut off" from browsing, instead an error page with header and footer appears and the user is informed of the situation.

- The following custom error pages were created :
  - 403 - Received when user attempts to access a web resource for which they lack the necessary permissions.
  - 404 - Encountered when the requested web resource by user is not found on the server.
  - 500 - Displayed when the web server encounters an internal error while processing the request.

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.1.5. Toasts**
- Toasts are used to communicate with the user. Four levels of toasts are in use (success, error, info and warning). Toasts do appear on the right top corner of the page with useful message for the user. Templates for toasts are under `templates/includes/toasts`. 

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **4.2. Main Content**

### **4.2.1. Landing Page**

- **App :** `home`
- **Template File :** `index.html` - extends `base.html`
- **User :** Provides the user with a clear understanding of what the page is about. The user is also provided with the latest jackpot details and the latest winning predictions of the jackpot in addition to a subscribe button and a 'How it Works' button for further explanation of the site-uses.
Since the Landing page is too large to be captured in a print screen, please refer to the [Landing Page](https://lottonero-e7dc9a7038d2.herokuapp.com/) here.

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.2.2. Subscriptions Page**

- **App :** `orders`
- **Template File :** `pricing_page.html` - extends `base.html`
- **User :** Provides the user with three types of subscriptions to choose from, 'AI Predictions for EuroMillions Lotto', 'Lotto Statistics for EuroMillions' and 'Premium Full Access' *( Appendix 29)*. 
- **Payment :** Since Subscriptions involve trial periods and recurrring payments and require significant management and maintenance time, Stripe will manage the payment and subscriptions untill Lottonero's extension of  dj-stripe is fully integrated in the future *( Appendix 30)*. However, in the meanntime, once a subscription payment is made, the subscribed user is redireted to Lottonero's success page with a session_id that writes the subscription details to the db to enable instantaneous access to their desired services *( Appendix 31)*. 

*Appendix 29 - Subscriptions Page*

![Subscriptions Page](/docs/features/subscriptions-page.JPG)

*Appendix 30 - Payment Page*

![Payment Page](/docs/features/payment-page.JPG)

*Appendix 31 - Payment Success Page*

![Payment Success Page](/docs/features/success-page.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.2.3. AI Predictions Pages**

- **App :** `predictions`
- **Template File :** `predictions.html` - extends `base.html`
- **User :** Provides the subscribed user with EuroMillions predictions using AI Patterns method which creates number patterns from the db holding the EuroMillions jackpot history *( Appendix 32)*. The user is then free to rely on these predictions while playing the EuroMillions lottery external to Lottonero.

*Appendix 32 - Predictions AI Patterns Page*

![Predictions AI Patterns Page](/docs/features/predict-patterns-page.JPG)

- **App :** `predictions`
- **Template File :** `combination_predictions.html` - extends `base.html`
- **User :** Provides the subscribed user with EuroMillions predictions using AI Combinations method which creates combinations from its own previous winning predictions *( Appendix 33)*. 
The user is then free to rely on these predictions while playing the EuroMillions lottery external to Lottonero.

*Appendix 33 - Predictions AI Combinations Page*

![Predictions AI Combinations Page](/docs/features/predict-combinations-page.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.2.4. Statistics Pages**

- **App :** `lottery-stats`
- **Template File :** `frequencies.html` - extends `base.html`
- **User :** Provides the user with two advance statictical frequency charts presenting highest ranking / winning ball numbers as well as median and KDE curves. This page features a dropdown selector to filter the graphs by quarterly time periods. Subscribed users are able to visualise the analytical data, thus enabling informed decisions when selecting their preferred numbers *( Appendix 34)*. Due to large graphic content of this page, a toast warning will pop up stating that this page is better viewed on larger screens.

*Appendix 34 - Frequencies Page*

![Frequencies Page](/docs/features/frequencies-page.JPG)

- **App :** `lottery-stats`
- **Template File :** `correlations.html` - extends `base.html`
- **User :** Provides the user with a statictical correlations heatmap presenting ball correlations from the jackpot history. This page features a mode-bar for graphical interactivity that enables the user to zoom / pan or capture a snapshot of the graph and more. Subscribed users are able to visualise the analytical data, thus enabling informed decisions when selecting their preferred numbers *( Appendix 35)*. Due to large graphic content of this page, a toast warning will pop up stating that this page is better viewed on larger screens.

*Appendix 35 - Correlations Page*

![Correlations Page](/docs/features/correlations-page.JPG)

- **App :** `lottery-stats`
- **Template File :** `combinations.html` - extends `base.html`
- **User :** Provides the user with a statictical combinations graph presenting ball combinations from the jackpot history. This page features a dropdown selector to filter the graphs by quarterly time periods and a mode-bar for graphical interactivity that enables the user to zoom / pan or capture a snapshot of the graph and more. Subscribed users are able to visualise the analytical data, thus enabling informed decisions when selecting their preferred numbers *( Appendix 36)*. Due to large graphic content of this page, a toast warning will pop up stating that this page is better viewed on larger screens.

*Appendix 36 - Combinations Page*

![Combinations Page](/docs/features/combinations-page.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.2.5. Alltime Hits Pages**

- **App :** `home`
- **Template File :** `alltime.html` - extends `base.html`
- **User :** Provides the user with a list of alltime winning predictions from the AI pattern predictions method *( Appendix 37)*. This page is accessible to site visitors for marketing purposes. This page is limited to 25 winning rows in order for Heroku not to time out. This page should be paginated as a future enhancement.

*Appendix 37 - Alltime AI Patters Page*

![Alltime AI Patters Page](/docs/features/alltime-patterns-page.JPG)

- **App :** `home`
- **Template File :** `alltime_shuffled.html` - extends `base.html`
- **User :** Provides the user with a list of alltime winning predictions from the AI combinations predictions method *( Appendix 38)*. This page is accessible to site visitors for marketing purposes. This page is limited to 25 winning rows in order for Heroku not to time out. This page should be paginated as a future enhancement.

*Appendix 38 - Alltime AI Patters Page*

![Alltime AI Combinations Page](/docs/features/alltime-combinations-page.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.2.6. About Page**

- **App :** `contact`
- **Template File :** `about.html` - extends `base.html`
- **User :**  Provides the user with information about the website *( Appendix 39)*.

*Appendix 39 - About Page*

![About Page](/docs/features/about-page.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.2.7. Contact Page**

- **App :** `contact`
- **Template File :** `contact.html` - extends `base.html`
- **User :**  Provides the user a form to complete and send a message to the website admin *( Appendix 40)*.
This page can recognise logged in users and use their logged in email with the form. Otherwise a logged out user or visitor will be prompted to enter their email before the massage is submitted /sent.

*Appendix 40 - Contact Page*

![Contact Page](/docs/features/contact-page.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.2.8. Backoffice Page**

- **App :** `predictions`
- **Template File :** `backoffice.html` - extends `base.html`
- **User :**  The Backoffice page button appears only to logged-in andmins. Once clicked, it displays a list with three command buttons with use-instructions *( Appendix 41)*.
This page allows the admin to scrape the EuroMillions jackpot details from the EuroMillions Accessible Results page, check the results against the predictions and update the home page accordingly. On this page is a 'Predict' button that creates the predictions for the upcoming draw using a datepicker. These two buttons in particular allow the admin to perform the core services for this website without having to do any manual input exceot for the winning anount of each winning prediction which will need to be added from Django's admin panel.
Should the developer be capable of scraping the winning amouts with the jackpot details, that would have required some major change to the db and as such was left as a future enhancement. 

*Appendix 41 - Backoffice Page*

![Backoffice Page](/docs/features/backoffice-page.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.2.9. My Profile Page**

- **App :** `user_profile`
- **Template File :** `profile.html` - extends `base.html`
- **User :**  Page where users can manage all aspects of their account including changing names, emails, password and subscription cancellation. *( Appendix 42)*.

*Appendix 42 - My Profile Page*

![Backoffice Page](/docs/features/profile-page.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.2.10. Forms**

- **App :** `AllAuth` extension
- **Template File :** `*.html` in `./templates/account` - extends `base.html`
- **User :** Forms do interact with user. They are designed to be clear and straight to the point, always in center of the screen. *( Appendix 43 )*.

*Appendix 43 - Forms*

![Forms](/docs/features/forms.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **4.2.11. User Emails**

- **App :** `orders`
- **Template File :** `*.html` in `./templates/emails`
- **User :** This project leverages user emails for muliple activities in association with AllAuth in addition to Subscription Success and Cancellation *( Appendix 44 )*.

*Appendix 44 - Email Sample*

![Email Sample](/docs/features/email.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **4.3. Future Features**

This project could be significantly improved by adding more features to include :

- Loader modals when pages are loading
- A designer logo
- Automated synchronisation with dj-stripe
- Functionality to scrape the win amounts with the jackpot details
- The pagination of Alltime pages
- Further research into AI robots that create predictions, from patterns and combinations

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

# **5. Marketing**

## **5.1. Social Media Presence**

[Lottonero Facebook Page](https://www.facebook.com/people/Lottonero/61561632711805/) was created in order to capture more online presence. The page will be used for adding posts to inform EuroMillios lottery enthusiast about our latest winning predictions. This will leverage the site's unique visitors count and generate more income. Facebook and other social platform do provide easy, cheap and effortless ways of advertisement *( Appendix 45 )*.

*Appendix 45 - Facebook Page*

![Facebook Page](/docs/fb-page.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **5.2. Search Engine Optimization (SEO)**

Key words within the **Lottonero** business scope were researched same as description tags. [Wordtracker](https://www.wordtracker.com/) was used to ensure that both short-tail and long-tail keywords are included. Keywords such as 'AI', 'EuroMIllions' and 'lotto' are aimed at reaching search queries within the business scope.

Files `sitemap.xml` and `robots.txt` were created to increase visibility of the site. These files are essential for SEO (Search Engine Optimization). The `sitemap.xml` file was generated using XML Sitemap and included in the root folder of the project. A robots.txt file was created in the root folder to instruct search engine crawlers on how to access and crawl the site's pages.

Page [XML-Sitemaps.com](https://www.xml-sitemaps.com/) was used to generate site map in `*.xml` format *( Appendix 46 )*.

*Appendix 46 - XML Site-map generator*

![XML Site-map generator](/docs/sitemap.JPG)

Once the file `robots.txt` was created, it was tested by [SEO AI](https://seo.ai/) *( Appendix 47 )*.

*Appendix 47 - Testing of `robots.txt`*

![Testing of robots.txt](/docs/robots.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

# **6. Validation, Testing & Bugs**

## **6.1. Validation**

Validation is documented separately in [validation.md](/docs/validation.md) file.

## **6.2. Testing**

Testing is documented separately in [testing.md](/docs/testing.md) file.

## **6.3. Bugs**

Bugs are documented separately in [bugs.md](/docs/bugs.md) file.

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

# **7. Deployment**

## **7.1. Transfer of progress from IDE**

- **Task :** To ensure regular commits are done to avoid any data/progress loss.
- **Method :** 
   - commands `git add [filename]` was used to add specific file to staging area, alternatively command `git add .` was used to add all changed files to staging area
   - command `git commit -m "[commit description]"` was used to add commitments into queue
   - command `git push` was used to push all commitments to remote repository on GitHub

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **7.2. Offline cloning**

- **Task :** To use repository on local machine.
- **Method :** 
  - Navigate to GitHub and follow `Code -> HTTPS -> Copy button` . after those steps open your local coding environment and type `git clone [copied link]`.

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **7.3. Deployment Prerequisites**

### **7.3.1. Microsoft O365**

- **Task :** Obtain email settings Microsoft Admin and enable SMTP to be used as mailing client.
- **Method :** 
  - Email settings
  - EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  - EMAIL_HOST = 'smtp.office365.com'
  - EMAIL_PORT = 587  # Use 465 for SSL or 587 for TLS
  - EMAIL_USE_TLS = True
  - EMAIL_USE_SSL = False
  - EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
  - EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
  - DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **7.3.2. Retool DB**

- **Task :** Obtain database URL to be used as project's database.
- **Method :** 
  - Select one of the DB providers, I did use [Retool](https://lottonero.retool.com/)
  - Navigate to `https://lottonero.retool.com/` and follow all steps for registering new account
  - Login to Retool DB Console with newly created account credentials
  - Navigate to `+ New Project`
  - Select `Name, Plan and Region`
  - Confirm the instance by pressing `Create Project`
  - Obtain database URL in format `postgresql://USERNAME:PASSWORD****************`
  - Update `settings.py` in the project directory
  - Update `env.py` with Retool username and password

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **7.3.3. Cloudinay Service**

- **Task :** Obtain Cloudinary Access Key and Secret Key in order to use Cloudinary to host media files on cloud storage
- **Method :** 
  - Cloudinary configuration
  - CLOUDINARY_STORAGE
  - 'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
  - 'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
  - 'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **7.3.4. Stripe Configuration & Connection**

- **Task :** Obtain all relevant settings and keys for online payments on project site
- **Testing :** - Dummy card details were used for testing purposes 4242 4242 4242 4242, expiry 04/24, cvc 242, zip 42424
- **Method :** 
  - Navigate to [Stripe](https://stripe.com/)
  - Create an account and login
  - Get your API keys (`STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY`)
  - Set those in your `env.py` for development and in Heroku vars for deployment
  - Install stripe by `pip install stripe` 
  - Create Webhook listeners
  - Add listener endpoint (URL for webhook listeners after deployment)
  - Add al keys to `env.py` and to Heroku config vars

*Appendix 57 - Webhook testing*

![Webhook testing](/docs/webhook-testing.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

### **7.3.5. Settings.py & file-tree**

- **Task :** Prepare `settings.py` adn file-tree for deployment 
- **Method :** 
  - Create file `env.py` to keep all sensitive information in
  - See example of `env.py` file *( Appendix 72 )*
  - Add `env.py` into `.gitignore` file to ensure this fill won't be uploaded to GitHub
  - update `settings.py` with `import os`
  - for every secured variable add code `VARIABLE = os.environ.get("VARIABLE")`
  - ensure this process for Microsoft Email, Retool DB, Cloudinary, DEBUG and Django Secret Key
 
[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **7.4. Deployment to Heroku**

- **Task :** To ensure users are able to view live version of **Lottonero** project.
- **Method :** 
  - Register & Log In with heroku
  - Navigate to `New > Create New App`
  - Select Name of the app that is unique
  - Navigate to `Settings > Reveal Config Vars`
  - Add all variables from `env.py` to ConfigVars of Heroku App *( Appendix 73)*
  - Add variable pair `PORT:8000`
  - For the testing deployment add variable pair `COLLECT_STATIC:1`
  - Add the Heroku app URL into `ALLOWED HOSTS` in `settings.py`
  - In root create file name `Procfile`
  - Navigate to `Deploy > GitHub > Connect`
  - Navigate to `Deploy > Deploy Branch`
  - Optionally, you can enable automatic deploys
  - See the deployment log - if the deployment was successful, you will be prompted with option to see live page

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

# **8. Technologies & Credits**

## **8.1. Technologies used to develop and deploy this project**

- [**Python**](https://www.python.org/) - main BackEnd programming language of the project
- [**HTML**](https://developer.mozilla.org/en-US/docs/Web/HTML) - templates programming language of this project (FrontEnd)
- [**CSS**](https://developer.mozilla.org/en-US/docs/Web/CSS) - styling the project via external CSS file `./static/css/style.css`
- [**Java Script**](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - dynamic templates programming language of this project (FrontEnd)
- [**jQuery**](https://api.jquery.com/) - API for JavaScript - dynamic templates programming language of this project (FrontEnd)
- [**Bootstrap v. 4**](https://getbootstrap.com/) - styling framework used in this project (FrontEnd)
- [**Heroku**](https://heroku.com) - to deploy this project
- [**Balsamiq**](https://balsamiq.com/support/) - to create wire-frames
- [**Git**](https://git-scm.com/doc) - to make commitments of progress and push the results back to GitHub
- [**GitHub**](https://github.com/) - to keep the track of version control
- [**Gitpod**](https://www.gitpod.io/) - Cloud IDE

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **8.2. Requirements.txt**

Following modules were used in development of **Lottonero** website :

- **asgiref==3.8.1**: ASGI (Asynchronous Server Gateway Interface) reference implementation and utilities, used for building asynchronous web applications in Python.
- **beautifulsoup4==4.11.1**: A library for parsing HTML and XML documents, useful for web scraping and data extraction.
- **black==24.4.2**: A code formatter for Python that enforces consistent code style.
- **blinker==1.8.1**: A fast, simple object-to-object and broadcast signaling library, often used for event handling.
- **channels==4.1.0**: Extends Django to handle WebSockets, HTTP2, and other protocols, enabling real-time functionality.
- **click==8.1.7**: A package for creating command-line interfaces with ease.
- **cloudinary==1.40.0**: A cloud-based service for managing images and videos, including storage, transformations, and delivery.
- **coverage==7.5.4**: A tool for measuring code coverage of Python programs, helpful for testing.
- **crispy-bootstrap4==2024.1**: Django app to manage forms, specifically integrating with the Bootstrap 4 framework.
- **dash==2.9.3**: A framework for building analytical web applications in Python.
- **dash-bootstrap-components==1.6.0**: Bootstrap components for use with Dash, making it easier to build responsive web applications.
- **dash-core-components==2.0.0**: Core set of components for building Dash applications, such as graphs and sliders.
- **dash-html-components==2.0.0**: HTML components for Dash, allowing for the integration of HTML tags within Dash applications.
- **dash-table==5.0.0**: Dash component for creating interactive tables in web applications.
- **dj-database-url==0.5.0**: Allows easy configuration of Django database connections using URL strings.
- **dj-stripe==2.8.4**: Integrates Stripe payments into Django applications.
- **Django==4.2.11**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **django-allauth==0.62.1**: An integrated set of Django applications addressing authentication, registration, account management, and more.
- **django-appconf==1.0.6**: A helper for handling configuration defaults of Django apps.
- **django-cloudinary-storage==0.3.0**: Django integration for Cloudinary file storage.
- **django-cors-headers==4.3.1**: Django app for handling the server headers required for Cross-Origin Resource Sharing (CORS).
- **django-crispy-forms==2.1**: Django app for building and managing forms, with support for various CSS frameworks.
- **django-environ==0.11.2**: Allows you to utilize 12-factor inspired environment variables to configure your Django application.
- **django-jazzmin==3.0.0**: A theme for Django admin that improves the interface's aesthetics and usability.
- **django-js-asset==2.2.0**: A Django app for managing JavaScript assets.
- **django-plotly-dash==2.3.1**: Integrates Dash applications into Django projects.
- **django-tinymce==4.0.0**: A Django application to use the TinyMCE editor for editing HTML content.
- **django-user-accounts==3.3.2**: A Django application for managing user accounts, including registration and authentication.
- **dpd_components==0.1.0**: A library for reusable, interactive components in Dash.
- **Flask==3.0.3**: A lightweight WSGI web application framework in Python, often considered a microframework.
- **gunicorn==20.1.0**: A Python WSGI HTTP Server for UNIX, designed for running Python web applications.
- **iniconfig==2.0.0**: A library for handling configuration files in .ini format.
- **itsdangerous==2.2.0**: A library for securely signing data, useful for tokens in web applications.
- **joblib==1.4.0**: A set of tools for lightweight pipelining in Python, used for parallel computing.
- **networkx==3.2.1**: A Python library for the creation, manipulation, and study of complex networks of nodes and edges.
- **numpy==1.26.4**: A fundamental package for scientific computing in Python, providing support for arrays and matrices.
- **oauthlib==3.2.2**: A library for creating OAuth clients and servers.
- **pandas==2.2.2**: A powerful data manipulation and analysis library for Python, providing data structures like DataFrames.
- **pathspec==0.12.1**: A utility library for pattern matching of file paths, used by tools like Black.
- **plotly==5.22.0**: A graphing library that makes interactive, publication-quality graphs online.
- **pluggy==1.5.0**: A plugin and hook calling mechanism for Python, used in various frameworks like pytest.
- **psycopg2==2.9.9**: PostgreSQL database adapter for Python.
- **python3-openid==3.2.0**: A library for OpenID authentication.
- **pytz==2024.1**: A library that allows accurate and cross-platform timezone calculations.
- **requests-oauthlib==2.0.0**: OAuth library support for Python requests.
- **scikit-learn==1.4.2**: A machine learning library for Python, providing simple and efficient tools for data mining and analysis.
- **scipy==1.13.0**: A Python library used for scientific and technical computing.
- **sqlparse==0.5.0**: A non-validating SQL parser for Python.
- **stripe==4.2.0**: Stripe API bindings for Python, facilitating payment processing.
- **tenacity==8.2.3**: A library for retrying code upon failure.
- **threadpoolctl==3.5.0**: A Python helper to control the number of threads in native libraries that are used for computations.
- **tzdata==2024.1**: A package that provides time zone database for date and time functionalities.
- **Werkzeug==3.0.2**: A comprehensive WSGI web application library for Python.
- **whitenoise==6.6.0**: A library for serving static files in production environments for Django.

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **8.3. Credits**

- [**Daisy McGirr**](https://www.linkedin.com/in/daisy-mcgirr/?originalSubdomain=uk) - brilliant mentor
- [**Elie Obeid**](https://parabim.ie/) - created background image and ball graphics
- [**Adobe Fonts**](https://fonts.adobe.com/) - used for picking the best typography
- [**Retool**](https://lottonero.retool.com/) - used as a database storage
- [**Cloudinary**](https://console.cloudinary.com/) - used as a storage of media files
- [**FavIcon.io**](https://favicon.io/favicon-converter/) - used to compress favicon
- [**Font Awesome Icons**](https://fontawesome.com/) - used to pick icons
- [**W3Schools**](https://www.w3schools.com/) - useful information and cheat sheets
- [**Markdown-Toc**](https://ecotrust-canada.github.io/markdown-toc/) - Table of contents generator
- [**XML-Sitemaps.com**](https://www.xml-sitemaps.com/) - XML Site-map generator
- [**Facebook**](https://www.facebook.com/profile.php?id=61556654592935) - Used as social media platform to promote the business goals
- [**SEO.AI**](https://seo.ai/) - `robots.txt` testing tool

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---
