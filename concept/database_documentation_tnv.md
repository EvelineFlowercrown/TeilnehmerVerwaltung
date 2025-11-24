# Database documentation: Teilnehmendenverwaltung

## participant_table

| Attribute      | Key | Data Type      | Description | 
|----------------|-----|-----------------|--------|
| p_id           | PK  | Integer         | participant ID |
| surname        | –   | String          | surname of participant |
| first_name     | –   | String          | first name of participant |
| btz_start      | –   | Date            | first day in BTZ | 
| btz_end        | –   | Date            | last day in BTZ | 
| pt_id          | FK  | Integer         | surname of professional trainer |
| ps_id          | FK  | Integer         | psychosocial associate ID |
| gdb            | –   | Boolean         | Grad der Behinderung = degree of diability >= 50  |
| bvb            | –   | Boolean         | berufsvorbereitende Bildungsmaßnahme = vocational preparation programm |
| seat           | –   | Integer         | seat of participant in the office |
| initials       | –   | String          | person who did the latest changes |
| birthday       | –   | Date            | birthday |
| birthday_list  | –   | Enum (yes, no, card)            | info if birthday can be announced in team or if p just wants a a card |
| table          | –   | Boolean         | medical certificate for a height-adjustable desk existent |
| measure        | –   | Enum (BT, BVB, FSM, KIM)        | rehabilitation measure |

---

## kitchen_duty_table

| Attribute | Key | Data Type | Description |
|-----------|-----|-----------|-------------|
| kd_id     | PK  | Integer   | kitchen duty ID
| kd_start     | –   | Integer       | first day of kitchen duty |

---

## assignment_table

| Attribute | Key | Data Type | Description |
|-----------|-----|-----------|-------------|
| p_id      | FK, PK  | Integer | participant ID
| kd_id     | FK, PK  | Integer | kitchen duty ID

---

## vacation_table

| Attribute       | Key | Data Type | Description |
|------------------|-----|-----------|------------|
| p_id             | FK, PK  | Integer | participant ID
| vacation_start   | PK   | Date       | first day of the vacation
| vacation_end     | –   | Date        | last day of vacation 

---

## internship_table

| Attribute        | Key | Data Type | Description |
|------------------|-----|-----------|-------------|
| p_id             | FK, PK  | Integer | participant ID
| internship_start | PK   | Date      | first day of internship |
| internship_end   | –   | Date      | last day of internship |
| btz_day          | –   | Enum (monday, tuesday, wednesday, thursday, friday) | weekday participant is in BTZ |

---

## ps_staff_table

| Attribute      | Key | Data Type |Description|
|----------------|-----|-----------|------------|
| ps_id          | PK  | Integer  | psychosocial associate ID |
| first_name_ps  | –   | String   | first name of psychosocial associate |
| surname_ps     | –   | String   | surname of psychosocial associate |

---

## pt_staff_table

| Attribute       | Key | Data Type | Description |
|------------------|-----|-----------|-------------|
| pt_id            | PK  | Integer  | professional trainer ID |
| first_name_pt    | –   | String   | first name of professional trainer |
| surname_pt       | –   | String   | surname of professional trainer |
