# Activity Calendar
A project made for a university database project course. Inspired by a work time system I used at a place of employment.

Heroku app: https://tsoha-activity-calendar.herokuapp.com/
## Intended use
The Activity Calendar can be used to keep track of activities, whether it's for private record keeping or for a team.

Example: Admin assigns different activities for a group of users to work on. One of them is titled "Work on user interface". When a user starts working on the user interface, they will mark "Work on user interface" as the current activity until they stop doing it. People within the group can look at the exact timestamps of when the user started working on the user interface and when they stopped it.
## Database tables
### Users
Will keep a record on usernames and hashed passwords. Also shows which group a user belongs to and whether they're an admin or a creator of that group. Each user is tied to a single group, so creating a new user is necessary to join multiple groups.
### Groups
Not assigning a user to a group will prompt the creation of a new group. Groups are used for internal communication between its members. Each group has at least a single admin user that can govern the group members. Activities are also group-specific.
### Activities
Will keep a record of activities, their names, creators and the group they're attached to. Admins can add any activities they want to use and users can submit activities for admin approval.
### UserActivities
Will attach an activity to a user. Also keeps track of the time when a user started an activity and the time when it was ended.
### Message Threads
Private message communications within a group are saved within threads. Each thread has a title that is visible within the user's inbox.
### Messages
Keeps a record of internal communication within a group. Saves the sender, the recipient, the thread the message is sent in, whether the recipient has read the message, and the message itself.
## User interface
The current version of the user interface can be tested [here](https://tsoha-activity-calendar.herokuapp.com/). The web app requires JavaScript to be enabled in order to function correctly.
### Home
Open the home page
### Log In
If you already have an account, you can log in through here. The log in button remains disabled until a username and password of a valid length are entered.
### Sign Up
If you do not have an account, one can be created here. Also prompts to assign a group for the new account. Selecting new group prompts to name the new group.
### Activities
Visible once logged in. Lists all activities of your group. Official Activities are created or approved by admins, activities Pending approval are created by regular members but have not yet been approved by admins. Admins can approve activities by pressing on _Approve Activity_ under _Activity Settings_. The page also allows you to create new activities. You can set activities as active by clicking on _Start this activity_ under the _Activity control_ column. If an activity is currently active, it, along with its starting time, is displayed at the top of the page. You can stop an activity by clicking on _Stop this activity_ under _Activity control_ column. Optionally, you can stop the activity and immediately start another one by clicking on _Stop current and start this activity_. If you are the creator of a pending activity or an admin, you can also change an activity's name or delete it.
### Inbox
Visible once logged in. Lists the discussions you've had with different members of your group. The page also lets you compose a new message to a member.
### Group
Visible once logged in. Lists all the members of your group, admins and regular members separately. You can also visit each member's profile to view their activity history (check the [Username section](https://github.com/Veloxization/activity-calendar#username) for more information on user profiles). As the creator of a group, you are able to promote members to admin, or strip them of their admin status. As an admin, you are able to delete regular members through their management page. Deleting a member also deletes any pending activities they've submitted so be sure to approve any activities you want to keep before deleting the member who submitted them! Just click on _Manage_ under the _Actions_ column to get to these settings. You can also message group members through here.
### Log Out
Visible once logged in. Log out from the current account.
### Username
Visible once logged in. Takes you to your own user profile. Within a user profile, you can view the user's ongoing activity (if any), their activity history, and, if you are an admin, you can also view the user's history in deleted activities. If you are the owner of the profile, you can also visit your settings page which allows you to change your password and delete your account. Deleting your account cannot be reversed and if you are the creator of a group, that group, along with its activities and members, will be permanently deleted. But don't worry, the website will show a confirmation prompt before letting you delete your account so accidental account deletions are less likely to happen.
