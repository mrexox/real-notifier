# Real Notifier

| **Type**  | Sender | Type | Value | Chk-sum | Ending |
|-----------+--------+------+-------+---------+--------|
| **Bytes** |      8 |    4 |    12 |       8 |      8 |

> 40 bits (5 bytes) 

* __Sender__ - is an object (mail, messenger or something else) that raised the message
* __Type__ - is the type of a message (incoming message, new friend and so on)
* __Value__ - is the count of new messages, friends and so on
* __Check-sum__ and __Ending__ - make the protocol more trustful

40 bytes are sent with every new type of event and source


