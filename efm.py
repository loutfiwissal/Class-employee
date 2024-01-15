from datetime import date

# Classe abstraite IR
class IR:
    tranches = [0, 28000, 40000, 50000, 60000, 150000]
    taux_IR = [0, 12, 24, 34, 38, 40]

    @staticmethod
    def get_IR(salaire):
        for i in range(len(IR.tranches) - 1):
            if salaire <= IR.tranches[i + 1]:
                return IR.taux_IR[i]
        return IR.taux_IR[-1]

# Interface IEmploye
class IEmploye:
    def Age(self):
        pass

    def Anciennete(self):
        pass

    def DateRetraite(self, ageRetraite):
        pass

# Classe Employe
class Employe(IEmploye):
    dernier_matricule = 0

    def _init_(self, nom, date_naissance, date_embauche, salaire_base):
        Employe.dernier_matricule += 1
        self.matricule = Employe.dernier_matricule
        self.nom = nom
        self.date_naissance = date_naissance
        self.set_date_embauche(date_embauche)
        self.salaire_base = salaire_base

    def set_date_embauche(self, date_embauche):
        age_a_embauche = self.Age()
        if age_a_embauche < 16:
            raise ValueError("L'employé doit avoir au moins 16 ans à la date d'embauche.")
        self.date_embauche = date_embauche

    def Age(self):
        today = date.today()
        return today.year - self.date_naissance.year - ((today.month, today.day) < (self.date_naissance.month, self.date_naissance.day))

    def Anciennete(self):
        today = date.today()
        return today.year - self.date_embauche.year

    def DateRetraite(self, ageRetraite):
        return self.date_naissance.year + ageRetraite

    def SalaireAPayer(self):
        pass

    def _str_(self):
        return f"{self.matricule}-{self.nom}-{self.date_naissance}-{self.date_embauche}-{self.salaire_base}"

    def _eq_(self, other):
        return self.matricule == other.matricule

# Classe Formateur
class Formateur(Employe):
    remuneration_h_sup = 70.00

    def _init_(self, nom, date_naissance, date_embauche, salaire_base, heure_sup):
        super()._init_(nom, date_naissance, date_embauche, salaire_base)
        self.heure_sup = heure_sup

    def SalaireAPayer(self):
        taux_IR = IR.get_IR(self.salaire_base + self.heure_sup * Formateur.remuneration_h_sup) / 100
        return (self.salaire_base + self.heure_sup * Formateur.remuneration_h_sup) * (1 - taux_IR)

    def _str_(self):
        return f"{super()._str_()}-{self.heure_sup}-{Formateur.remuneration_h_sup}"

# Classe Agent
class Agent(Employe):
    def _init_(self, nom, date_naissance, date_embauche, salaire_base, prime_responsabilite):
        super()._init_(nom, date_naissance, date_embauche, salaire_base)
        self.prime_responsabilite = prime_responsabilite

    def SalaireAPayer(self):
        taux_IR = IR.get_IR(self.salaire_base + self.prime_responsabilite) / 100
        return (self.salaire_base + self.prime_responsabilite)*(1-taux_IR)
