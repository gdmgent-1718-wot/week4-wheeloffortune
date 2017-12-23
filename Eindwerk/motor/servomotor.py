import machine
pin = machine.pin(4)
servo = machine.PWM(pin, freq=50)

servo.duty(40)
servo.duty(115)
servo.duty(77)





