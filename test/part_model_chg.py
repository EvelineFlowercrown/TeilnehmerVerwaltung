#ModelsPy
from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from database import BaseClass

class Participants(BaseClass)
    __tablename__= "participants_table"

    p_id:Mapped[int]= mapped_column(nullable= False,primary_key= True, autoincrement = True )

    #Name Sur and First and GDB; not Null
    surname:Mapped[str]= mapped_column( nullable= False)
    first_name:Mapped[str]= mapped_column( nullable= False)



    #Start  End Measure
    btz_start:Mapped[Date]= mapped_column(nullable= False)
    btz_ende:Mapped[Date]= mapped_column(nullable= False)

    #Staff BTZ
    pt_id:Mapped[int]= mapped_column(ForeignKey("pt_staff.pt_id"))
    ps_id:Mapped[int]= mapped_column(ForeignKey("ps_staff.ps.id"))

    #Needs Professional-Trainer and Psychosocial-Trainer
    gdb: Mapped[int] = mapped_column(nullable=True)
    bvb:Mapped[Boolean]= mapped_column(nullable= True)
    seat:Mapped[int] = mapped_column(nullable=True)
    initials:Mapped[int] = mapped_column(nullable=True)
    table:Mapped[Boolean] = mapped_column(nullable=True)
    measure:Mapped[Boolean] = mapped_column(nullable=False)


    #Birthdays
    birthday:Mapped[Date] = mapped_column(nullable=True)
    birthday_list:Mapped[Boolean] = mapped_column(nullable=True)

class Vaction(BaseClass)
    __tablename__= "vacation"

    #Vacation Start and End + participants.p_id
    p_id:Mapped[int]= mapped_colum(ForeignKey("participans.p_id"),nullable=False)
    vacation_start:Mapped[Date]= mapped_column(nullable= False)
    vacation_end:Mapped[Date]= mapped_column(nullable= False)

#Relationship- participants 1: N  vacation(takes vacation)
vacation:Mapped["vacation"]= relationship( back_populates= "paticipants")

class PsStaff(BaseClass)
    __tablename__= "ps_staff"
    ps_id:Mapped[int]= mapped_column(nullable= False,primary_key= True, autoincrement = True )
    first_name_ps:Mapped[str]= mapped_column( nullable= False)
    surname_ps:Mapped[str]= mapped_column( nullable= False)


    #Realtionships
    #
    #- participants N: 1 ps_staff(supervised by)
    #- participants N: 1 pt_staff(supervised by)
    #- participants 1: N internship(does an internship)
    #- participants 1: N assignment - kitchen_duty 1: N assignment



    intership:Mapped["intership"]= relationship( back_populates= "paticipants")
    assigment:Mapped["assigment"]= relationship( back_populates= "paticipants")


class KitchenDuty(Base):
    __tablename__ = "kitchen_dutys_table"

    kd_id: Mapped[str] = mapped_column(primary_key=True)
    cw_id: Mapped[int] = mapped_column(nullable=False)
    participants: Mapped[List[Participant]] = relationship(
        secondary=assignments_table, back_populates="kitchen_duties"
    )


class Assignment(Base):
    __tablename__ = "assignments_table"
    p_id: Mapped[int] = mapped_column(
        ForeignKey("participants_table.p_id"), primary_key=True, nullable=False
    )
    kd_id: Mapped[int] = mapped_column(
        ForeignKey("kitchen_dutys_table.ki_id"),
        primary_key=True,
        nullable=False,
    )
    participants: Mapped["Participant"] = relationship(
        back_populates="assignments"
    )
    kitchen_duties: Mapped["KitchenDuty"] = relationship(
        back_populates="assigments"
    )


class Internship(Base):
    __tablename__ = "internships_table"
    p_id: Mapped[int] = mapped_column(
        ForeignKey("participants_table.p_id"), primary_key=True, nullable=False
    )
    internship_start: Mapped[date] = mapped_column(
        Date, primary_key=True, nullable=False
    )
    internship_end: Mapped[Date] = mapped_column(nullable=False)
    btz_day: Mapped[int] = mapped_column(nullable=False)


class PtStaff(Base):
    __tablename__ = "pt_staff_table"
    pt_id: Mapped[int] = mapped_column(
        ForeignKey("participants_table.p_id"), primary_key=True, nullable=False
    )

