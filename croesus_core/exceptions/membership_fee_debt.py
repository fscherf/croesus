class MembershipFeeDebtError(Exception):
    pass


class MultipleMembershipFeeDebtsError(Exception):
    def __init__(self, person, period):
        self.person = person
        self.period = period
