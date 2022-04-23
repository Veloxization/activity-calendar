# Activity Calendar
A project made for a university database project course. Inspired by a work time system I used at a place of employment.

Heroku app: https://tsoha-activity-calendar.herokuapp.com/
## Intended use
The Activity Calendar can be used to assign and keep track of activities, whether it's for private record keeping or for a team.

For example: User is supposed to be working on a user interface from 8 AM to 12 PM, Admin assigns "Work on user interface" to the time slot 8 AM to 12 PM for User. User marks "Work on user interface" as the active activity at 8 AM and marks it as done at 12 PM.
## Database tables
### Users
Will keep a record on usernames and hashed passwords. Also shows which group a user belongs to and whether they're an admin of that group. As of now, each user is tied to a single group, so creating a new user is necessary to join multiple groups. Similarly, deleting the account used in group creation also deletes the group and all its members.
### Groups
Not assigning a user to a group will prompt the creation of a new group. Groups are used for internal communication between its members. Each group has at least a single admin user that can govern the group members. Activities are also group-specific.
### Activities
Will keep a record of activities, their names, creators and the group they're attached to. Admins can add any activities they want to use and users can submit activities for admin approval.
### UserActivities
Will attach an activity to a user. Also keeps track of the time when a user started an activity and the time when it was ended.
### ActivityGoals
The goal start times and end times for different activities for different users. Set up by group admins.
### Messages
Keeps a record of internal communication within a group. Saves the sender, the recipient and the message.
## User interface
The current version of the user interface can be tested [here](https://tsoha-activity-calendar.herokuapp.com/). The web app requires JavaScript to be enabled in order to function correctly.
### Home
Open the home page
### Log In
If you already have an account, you can log in through here. The log in button remains disabled until a username and password of a valid length are entered.
### Sign Up
If you do not have an account, one can be created here. Also prompts to assign a group for the new account. Selecting new group prompts to name the new group.
### Activities
Visible once logged in. Lists all activities of your group. Official Activities are created or approved by admins, activities Pending approval are created by regular members but have not yet been approved by admins. The page also allows you to create new activities. You can set activities as active by clicking on _Start this activity_ under the _Activity control_ column. If an activity is currently active, it, along with its starting time, is displayed at the top of the page. You can stop an activity by clicking on _Stop this activity_ under _Activity control_ column. Optionally, you can stop the activity and immediately start another one by clicking on _Stop current and start this activity_.
### Inbox
Visible once logged in. **Currently unavailable.** Lists the discussions you've had with different members of your group. The page also lets you compose a new message to a member.
### Group
Visible once logged in. Lists all the members of your group, admins and regular members separately. In the future you will be able to message group members through here, or manage them if you're an admin.
### Log Out
Visible once logged in. Log out from the current account.
### Username
Visible once logged in. Allows you to change your password or delete your account. Deleting the account that created a group will also take down the entire group, all of its activities and members. This _cannot_ be reversed.
