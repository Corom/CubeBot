using Iot.Device.BuildHat;

Console.WriteLine("Hello, World!");

using(Brick brick = new("/dev/serial0")) {
    var info = brick.BuildHatInformation;
    Console.WriteLine($"version: {info.Version}, firmware date: {info.FirmwareDate}, signature:");
    Console.WriteLine($"{BitConverter.ToString(info.Signature)}");
    Console.WriteLine($"Vin = {brick.InputVoltage.Volts} V");
}

