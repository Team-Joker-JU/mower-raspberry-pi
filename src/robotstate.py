class RobotState:    
    _paired = True

    def is_paired(self) -> bool:
        return self._paired
    
    def set_paired(self, state: bool):
        self._paired = state