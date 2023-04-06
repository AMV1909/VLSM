from math import floor


def initialIP():
    print("Ingrese IP inicial")
    IP = []
    ip = input("IP: ")
    subnet = []

    # Validar IP
    for i in ip.split("."):
        if int(i) < 0 or int(i) > 255:
            print("IP inválida")
            initialIP()
        else:
            IP.append(i)

    print("\nIngrese máscara de red (prefijo)")
    prefix = int(input("Prefijo: "))

    # Validar prefijo
    # La máxima cantidad de bits disponibles en IPv4 es 32
    while (prefix < 0 or prefix > 32):
        print("Prefijo inválido")
        prefix = int(input("Prefijo: "))

    print("\n" + ".".join(IP) + "/" + str(prefix))

    # El prefijo es la cantidad de 1's en la máscara de red
    # El resto de los bits son 0's
    maskBinary = "1" * prefix + "0" * (32 - prefix)
    maskBinary = f"{maskBinary[0:8]}.{maskBinary[8:16]}.{maskBinary[16:24]}.{maskBinary[24:32]}"
    print("Máscara de red (Binario): " + maskBinary)

    # Convertir máscara de red binaria a decimal
    mask = [str(int(i, 2)) for i in maskBinary.split(".")]
    print("Máscara de red: " + ".".join(mask))

    # Calcular cantidad de bits disponibles para robar
    bitsAvailable = maskBinary.count("0")

    # Calcular cantidad de subredes
    # La cantidad de subredes es 2^bits disponibles para robar
    subnetLength = int(input("\nIngrese la cantidad de subredes: "))
    while (subnetLength < 1 or subnetLength > 2**(bitsAvailable)):
        print("Cantidad de subredes inválida")
        subnetLength = int(input("Ingrese la cantidad de subredes: "))

    # Calcular cantidad de hosts por subred
    # La cantidad de hosts por subred es 2^bits disponibles para robar - 2
    # La cantidad de bits disponibles para robar se va reduciendo a medida que se asignan hosts a las subredes
    print("\nIngrese la cantidad de hosts por subred")

    # Variables auxiliares para calcular la cantidad de bits disponibles para robar
    # Se usan para no modificar las variables originales
    prefixAux = prefix
    bitsAvailableAux = bitsAvailable
    for i in range(subnetLength):
        subnet.append(int(input(f"Subred {str(i + 1)}: ")))

        # Validar cantidad de hosts
        # La cantidad de hosts por subred debe ser menor a 2^bits disponibles para robar - 2
        # -2 porque la primera y última IP de la subred no se pueden usar, ya que son la IP de la subred y la IP de broadcast
        while (subnet[i] < 1 or subnet[i] > 2**(bitsAvailableAux) - 2):
            print("Cantidad de hosts inválida")
            subnet[i] = int(input(f"Subred {str(i + 1)}: "))

        # Restar los bits usados a los bits disponibles para robar
        h = 0

        while (2**h - 2 < subnet[i]):
            h += 1

        # Si se han asigando una cantidad de hosts cercana a la cantidad máxima de hosts por subred
        # Se asigna un solo bit para robar, ya que es el mínimo que se puede asignar a una subred
        n = bitsAvailableAux - h if bitsAvailableAux - h > 0 else 1
        prefixAux += n
        bitsAvailableAux -= n

    # Oredenar de mayor a menor
    subnet.sort(reverse=True)
    print(f"\nSubredes: {subnet}")

    CalculateSubnet(IP, mask, prefix, subnet, bitsAvailable)


def CalculateSubnet(IP, mask, prefix, subnet, bitsAvailable):
    for i in range(len(subnet)):
        h = 0

        # Buscar h para calcular la cantidad de bits disponibles para robar
        while (2**h - 2 < subnet[i]):
            h += 1

        # Restar los bits usados a los bits disponibles para robar
        n = bitsAvailable - h if bitsAvailable - h > 0 else 1
        prefix += n
        bitsAvailable -= n

        # Calcular máscara de red
        maskBinary = "1" * (32 - bitsAvailable) + "0" * bitsAvailable
        maskBinary = f"{maskBinary[0:8]}.{maskBinary[8:16]}.{maskBinary[16:24]}.{maskBinary[24:32]}"
        mask = [str(int(i, 2)) for i in maskBinary.split(".")]

        # Calcular cuál es el último octeto de la máscara de red con la cantidad de bits disponibles para robar
        lastOctet = -floor(bitsAvailable / 8) - 1
        magicNumber = 256 - int(mask[lastOctet])

        print(f"\nSubred {i + 1}: {subnet[i]} hosts")
        print("Máscara de red: " + ".".join(mask))
        print(f"\nh = {h} => 2^{h} - 2 = {2**h - 2} hosts")
        print(f"n = {n} => 2^{n} = {2**(n)} subredes")
        print(
            f"m = {magicNumber} => 256 - {mask[-floor(bitsAvailable / 8) - 1]} = {magicNumber}\n")

        # Imprimir redes y rangos
        IP_copy = IP.copy()
        for j in range(2**(n)):
            # Sumar j al último octeto de la IP multiplicando por el número mágico
            # El número mágico son los saltos que se deben dar para llegar a la siguiente subred
            IP_copy[lastOctet] = str(int(IP[lastOctet]) + j * magicNumber)

            # Calcular el primer host y el último host de la subred

            # Dependiendo de cuál sea el último octeto de la máscara de red
            # Se buscará copiar toda la IP
            # Si el último octeto del que se están robando bits es el penúltimo
            # Se se le sumará 1 al valor de lastOctet para copiar toda la IP
            # Si el último octeto es el último, se copiará la IP simplemente
            firstHost = IP_copy[0:lastOctet + 1] if lastOctet + \
                1 < 0 else IP_copy[0:lastOctet]

            # Se le suma 1 al último octeto de la IP
            firstHost.append(str(int(
                IP_copy[lastOctet + 1]) + 1 if lastOctet + 1 < 0 else int(IP_copy[lastOctet]) + 1))

            # Igual que la del firstHost, se busca copiar toda la IP
            lastHost = IP_copy[0:lastOctet + 1] if lastOctet + \
                1 < 0 else IP_copy[0:lastOctet]

            # Se le resta 1 al último octeto de la IP
            octecLastHost = int(
                IP_copy[lastOctet + 1]) - 1 if lastOctet + 1 < 0 else int(IP_copy[lastOctet]) + magicNumber - 2

            # Si el último tiene un valor negativo, se le suma 255 para que sea un valor válido
            lastHost.append(
                str(octecLastHost + 255 if octecLastHost < 0 else octecLastHost))

            # Si el último octeto del que se están robando bits es el penúltimo, se le suma el número mágico y se le resta 1
            # Para así obtener el último host de la subred
            lastHost[lastOctet] = str(int(
                lastHost[lastOctet]) + magicNumber - 1 if lastOctet + 1 < 0 else int(lastHost[lastOctet]))

            # Broadcast
            # Sólo se copia la IP del último host y se le suma 1 al último octeto
            broadcast = lastHost[0:3] + [str(int(lastHost[3]) + 1)]

            # Si algún octeto de la IP es mayor a 255, se le suma 1 al anterior y se le resta 256 al actual
            for k in range(3, -1, -1):
                if int(IP_copy[k]) > 255:
                    IP_copy[k - 1] = str(int(IP_copy[k - 1]) + 1)
                    IP_copy[k] = str(int(IP_copy[k]) - 256)

                if int(firstHost[k]) > 255:
                    firstHost[k - 1] = str(int(firstHost[k - 1]) + 1)
                    firstHost[k] = str(int(firstHost[k]) - 256)

                if int(lastHost[k]) > 255:
                    lastHost[k - 1] = str(int(lastHost[k - 1]) + 1)
                    lastHost[k] = str(int(lastHost[k]) - 256)

                if int(broadcast[k]) > 255:
                    broadcast[k - 1] = str(int(broadcast[k - 1]) + 1)
                    broadcast[k] = str(int(broadcast[k]) - 256)

            print(".".join(IP_copy) + "/" +
                  str(prefix) + " => " + ".".join(firstHost) + "/" + str(prefix) + " - " + ".".join(lastHost) + "/" + str(prefix) + " <= " + ".".join(broadcast) + "/" + str(prefix))

            # Si se está haciendo la segunda iteración, la IP de subred se asigna a la IP de la red siguiente
            if j == 1:
                IP = IP_copy.copy()


initialIP()
input()
