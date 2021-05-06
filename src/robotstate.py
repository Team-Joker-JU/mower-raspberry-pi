class RobotState:    
    _paired = False

    def is_paired(self) -> bool:
        return self._paired
    
    def set_paired(self, state: bool):
        self._paired = state