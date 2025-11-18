from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship, MappedColumn, Mapped
from database import BaseClass


# =========================================================
#   TEILNEHMENDER  (Hauptperson)
# =========================================================
class Teilnehmender(BaseClass):
    __tablename__ = "teilnehmende"

    tn_id: Mapped[int] = MappedColumn(Integer, primary_key=True)

    # Stammdaten
    nachname = Column(String)
    vorname = Column(String)

    # BTZ-Daten
    btz_start = Column(Date)
    btz_ende = Column(Date)
    massnahme = Column(String)
    bvb = Column(Boolean)

    # Betreuer-IDs
    bt_id = Column(Integer, ForeignKey("bt_mitarbeiter.bt_id"))
    ps_id = Column(Integer, ForeignKey("ps_mitarbeiter.ps_id"))

    # Bedürfnisse
    gdb = Column(Boolean)
    sitzplatz = Column(String)
    tisch_verstellbar = Column(Boolean)

    # Geburtstag
    geburtstag = Column(Date)
    geburtstagsliste = Column(Boolean)

    kuerzel = Column(String)

    # Beziehungen zu Betreuern
    bt_mitarbeiter = relationship("BT_Mitarbeiter", back_populates="teilnehmende")
    ps_mitarbeiter = relationship("PS_Mitarbeiter", back_populates="teilnehmende")

    # 1:N-Beziehungen
    urlaube = relationship("Urlaub", back_populates="teilnehmer")
    praktika = relationship("Praktikum", back_populates="teilnehmer")
    einsaetze = relationship("Einsatz", back_populates="teilnehmer")


# =========================================================
#   URLAUB  (Urlaub eines Teilnehmenden)
# =========================================================
class Urlaub(BaseClass):
    __tablename__ = "urlaub"

    tn_id = Column(Integer, ForeignKey("teilnehmende.tn_id"), primary_key=True)
    urlaub_start = Column(Date, primary_key=True)
    urlaub_ende = Column(Date)

    # gehört zu genau einem Teilnehmenden
    teilnehmer = relationship("Teilnehmender", back_populates="urlaube")


# =========================================================
#   KUECHENDIENST (Unabhängig)
# =========================================================
class Kuechendienst(BaseClass):
    __tablename__ = "kuechendienst"

    kd_id = Column(Integer, primary_key=True)
    kw_kd = Column(Integer)


# =========================================================
#   PRAKTIKUM (1:N zu Teilnehmender)
# =========================================================
class Praktikum(BaseClass):
    __tablename__ = "praktikum"

    tn_id = Column(Integer, ForeignKey("teilnehmende.tn_id"), primary_key=True)
    praktikum_start = Column(Date, primary_key=True)
    praktikum_ende = Column(Date)
    btz_tag = Column(String)

    teilnehmer = relationship("Teilnehmender", back_populates="praktika")


# =========================================================
#   BT-MITARBEITER (Betreuer)
# =========================================================
class BtMitarbeiter(BaseClass):
    __tablename__ = "bt_mitarbeiter"

    bt_id = Column(Integer, primary_key=True)
    nachname = Column(String)
    vorname = Column(String)
    kuerzel = Column(String)

    # alle Teilnehmenden, die diesen Betreuer haben
    teilnehmende = relationship("Teilnehmender", back_populates="bt_mitarbeiter")


# =========================================================
#   PS-MITARBEITER (Pädagogischer Mitarbeiter)
# =========================================================
class PsMitarbeiter(BaseClass):
    __tablename__ = "ps_mitarbeiter"

    ps_id = Column(Integer, primary_key=True)
    nachname = Column(String)
    vorname = Column(String)
    kuerzel = Column(String)

    teilnehmende = relationship("Teilnehmender", back_populates="ps_mitarbeiter")


# =========================================================
#   EINSATZ (Arbeits-/Praktikums-Einsatz)
# =========================================================
class Einsatz(BaseClass):
    __tablename__ = "einsatz"

    einsatz_id = Column(Integer, primary_key=True)

    tn_id = Column(Integer, ForeignKey("teilnehmende.tn_id"))
    kw = Column(Integer)

    bt_id = Column(Integer, ForeignKey("bt_mitarbeiter.bt_id"))
    ps_id = Column(Integer, ForeignKey("ps_mitarbeiter.ps_id"))
    beschreibung = Column(String)

    teilnehmer = relationship("Teilnehmender", back_populates="einsaetze")
    bt_mitarbeiter = relationship("BT_Mitarbeiter")
    ps_mitarbeiter = relationship("PS_Mitarbeiter")
