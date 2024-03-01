# Violets-club

This project is the implementation of a club of violet lovers with access to view the site's pages for all users.

The project realizes convenient navigation for switching from the home page to other pages
with a list of violet species, club members and plants. 

Detailed information about plants and club members is shown on the respective pages. 

To develop the project, there are functions like creation of new members, varieties, 
add violets of new varieties, although this functionality is available only for registered users. 

The site admin has an additional option to edit the "Tip of the day" section. 

(The creation of new tips is hidden, because the daily variability is implemented 
through the tip id, i.e. id > 31 will never be completed). 

Club members can change their own list of violets through an additional function both on 
page violet and from the page with a list of all violets. 

Also, through open contacts, users can contact with each other to buy, exchange and gift plants. 

To make hobby even more interesting, there is a "Top Collection" section on the home page. 

To install via GitHub, run the following commands: 

git clone https://github.com/NPovashevych/Violets-club.git
git checkout -b develop
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt 

After installing all the necessary applications, you need to execute the commands to deploy and start the project: 

python manage.py migrate
python manage.py runserver

Check it out!
https://violets-club-2.onrender.com/

test user:
login - its_me
password - !adm123in
