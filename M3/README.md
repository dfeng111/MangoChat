## Design Patterns
Creational Patterns

1) Singleton

We can utilize the singleton methods for ensuring there is one instance of a specific user this will insure that no duplicate instances of a user occur within the program, This helped since we do not 
have a need to utilize multiple instances of the same user as well as it helped with user security. Furthermore, we can utilize simpleton methods to ensure the instance of 1 admin user per chat room 
since from my understanding we only need to have 1 admin user per room and when appointing a new admin for a room the previous admin looses their permissions.
2) Abstract factory method

USeful for the facilitation of Chatroom classes as well as the the creating of user and Admin classes since these classes would share functionality and behaviour accross multiple instances of the objects.
"Abstract Factory method or Abstract Factory Design Patterns provides for creating families of related or dependent objects without specifying their concreate class. It is also knows as Kit." 
Both user and Admin users are utlizing the same functionality as each other but admin would have greater permissions within a chatroom itself, therefore they are within the same "family" as a user and 
utilize the same related classes across the entirety of the program.

2) Abstract Factory methods could also be utilized in facilitation of who is in what chat room since the connected users would be contained under the same family of objects utilizing the same class 
for the rooms istself as well as for assigning which users are in which rooms.



 Behavioral Patterns 

3) Observer methods

Observer methods are good for alteration made to the user & admin classes since admin classes share functionality with user and would need to be updated with the same features as the user classes
should updates occur. we would also requre both user and admin objects to update to constraints provided by the channels created, joined and left. This will esure smooth implementation of updates to 
features users can access as well as I will ensure admin users gain new functionality when channels are updated with new controls and that users recieve constraints to channels they are involved in
when new updates to the application are implemented or admins update contraintes/rules for the channels in question.


## Testing Plan 

Our test plan will be to unit test, integration test, system test and acceptance test.
In our pull requests unit testing will be included. We will run regression testing.
For unit testing we will test the smallest piece of code(function or method) in the application.
For integration testing individual software modules will be combined then tested as a group.
For system testing it will be tested when our system is complete in order to evaluate it.
For acceptance testing we will check for flaws and confirm that our system meets its requirements.
We will run regression testing to ensure that after every change there are no unintended breaks.

##Sequence Diagrams 
### Registration
![Registration Sequence Diagram](M3/MangoSeqDiagram.png)

### Sending messages
![Sending Messages Sequence Diagram](M3/Sending Message Diagram.png)

## Class Diagram
![Mango Chat Class Diagram](M3/MangoClassDiag.png)
