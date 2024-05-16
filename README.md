# RPT
Resource Planning Tool

Slot based resource planning tool.

The Resource slot has fields with headers and the purpose as below. The header started with a "*" are required when creating a resource slot: 
- *ID : Auto generated unique ID as an identifier. Not editable.
- *Type : Any type to identify the purpose of the resource request.
- Category : Categorise the resource
- Tag : Any identification which can be use for quering the required resource
- *Start : start date 
- *End : End date
- Owner : a person who aquire the resource
- *Preserve period : the time period in days which the resource will be reserved for the owner before the start date.
- Status : Three state with Live, Pending, Assigned, Used or Perished. Default as Live apon creation.

The Resource Manager can do following actions to the slot
- Query : Use nature language to query the existing resource from the database
- Create : Crete a resource slot with nature language 
- Modify : Use nature language to modify any of the fields for a resource slot except the *ID.
- Remove : Remove a slot from a database. Need to get the reconfirmation from the Resource Manager.

The Resource Requester can do following actions to the slot
- Query : Use nature language to query the existing resource from the database
- Request : Change to change the resource owner. 

![image](https://github.com/wj1313677/RPT/assets/1673691/9719afce-2b5b-43f1-8ffb-2544242ac705)



