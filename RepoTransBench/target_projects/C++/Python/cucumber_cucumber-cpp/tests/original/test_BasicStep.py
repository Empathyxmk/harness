import pytest

class InvokeResult:
    def __init__(self, pending=False, description=''):
        self._pending = pending
        self._desc = description
    def isPending(self):
        return self._pending
    def getDescription(self):
        return self._desc

class GenericStep:
    def __init__(self):
        self.args = None
    def pending(self, desc=None):
        if desc:
            raise StepPendingError(desc)
        else:
            raise StepPendingError("")
    def invoke(self, args):
        try:
            self.body()
            return InvokeResult(False, "")
        except StepPendingError as e:
            return InvokeResult(True, str(e))
    def body(self):
        pass

class StepPendingError(Exception):
    pass

PENDING_STEP_DESCRIPTION = "A description"

class PendingStep(GenericStep):
    def body(self):
        self.pending()
class PendingStepWithDescription(GenericStep):
    def body(self):
        self.pending(PENDING_STEP_DESCRIPTION)

NO_INVOKE_ARGS = ()

def test_handles_pending_steps():
    pendingStep = PendingStep()
    pendingStepWithDescription = PendingStepWithDescription()
    result = pendingStep.invoke(NO_INVOKE_ARGS)
    assert result.isPending()
    assert result.getDescription() == ""
    result = pendingStepWithDescription.invoke(NO_INVOKE_ARGS)
    assert result.isPending()
    assert result.getDescription() == PENDING_STEP_DESCRIPTION