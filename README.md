# Activity Calendar
A project made for a university database project course. Inspired by a work time system I used at a place of employment.
## Intended use
The Activity Calendar can be used to assign and keep track of activities, whether it's for private record keeping or for a team.

For example: User is supposed to be working on a user interface from 8 AM to 12 PM, Admin assigns "Work on user interface" to the time slot 8 AM to 12 PM for User. User marks "Work on user interface" as the active activity at 8 AM and marks it as done at 12 PM.
## Database tables
### Users
Will keep a record on usernames, email addresses, and hashed passwords. Also shows which group a user belongs to and whether they're an admin of that group.
### Groups
Creating a new admin account will prompt the user to create a new group. Groups are used for internal communication between its members. Each group has at least a single admin user that can govern the group members.
### Activities
Will keep a record of activities, mainly their names. It is intended that admins can add any activities they want to use and users can submit activities for admin approval.
### UserActivities
Will attach an activity to a user. Also keeps track of the time when a user started an activity and the time when it was ended.
### ActivityGoals
The goal start times and end times for different activities for different users. Set up by group admins.
### Messages
Keeps a record of internal communication within a group. Saves the sender, recipient and the message.