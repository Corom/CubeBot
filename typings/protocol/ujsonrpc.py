
class JSONRPC:
    methods:dict

    def emit(message:str, params:any = None) -> None:
        """
        Sends a RPC message

        Parameters
        -------------
        message : name of the message
        params : parameter object to pass to the message
        """
        pass

    def add_method():
        """
        Retrieves the position of the motor. This is the clockwise angle between the moving marker and the zero-point marker on the motor.
        
        Returns
        ----------
        The position of the motor
        
        Type : integer (positive or negative whole number, including 0)
        
        Values : 0 to 359 degrees
        
        Errors
        ------------
        RuntimeError : The motor has been disconnected from the Port.
        """
        pass

json_rpc:JSONRPC