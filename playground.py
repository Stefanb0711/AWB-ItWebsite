import dns.resolver

def check_email_domain(email):
    try:
        domain = email.split('@')[1]
        dns_abfrage = dns.resolver.resolve(domain, 'MX')
        print("DNS-Abfrage war erfolgreich für die Domain:", domain)
        return True
    except dns.resolver.NoAnswer:
        print("Es gibt keinen MX-Eintrag für die Domain:", domain)
        return False
    except dns.resolver.NXDOMAIN:
        print("Die Domain existiert nicht:", domain)
        return False
    except dns.resolver.Timeout:
        print("Zeitüberschreitung bei der DNS-Auflösung für die Domain:", domain)
        return False
    except Exception as e:
        print("Ein unerwarteter Fehler ist aufgetreten:", str(e))
        return False

# Beispielaufruf
email = "shwuqhsu@awbit.de"
print("Ist die Domain der E-Mail potenziell vorhanden?", check_email_domain(email))
