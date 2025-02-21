
if __name__ == "__main__":

    printer_layers = [5,4,4]

    for k in range(len(printer_layers)):
        is_greater = any(printer_layers[k] > value for value in printer_layers[:k] + printer_layers[k+1:])
        if is_greater:
            print(f"Printer {k} (Layer {printer_layers[k]}) is greater than at least one other printer.")
        else:
            print(f"Printer {k} (Layer {printer_layers[k]}) is not greater than any other printer.")
