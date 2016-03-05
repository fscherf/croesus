class MembershipFeeAgreementError(Exception):
    pass


class MultipleMembershipFeeAgreementsError(MembershipFeeAgreementError):
    def __init__(self, agreements):
        self.agreements = agreements
