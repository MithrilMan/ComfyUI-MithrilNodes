# nodes/utils.py
import inspect

NODES_PREFIX = "Ⓜ️ "


class Categories:
    """
    Contain the strings for the categories of MithrilNodes nodes.
    This prevents typos and centralizes the management of names.
    """

    # Main category
    MAIN = NODES_PREFIX + "MithrilNodes"

    # Subcategories
    DEBUG = f"{MAIN}/Debug"
    UTILS = f"{MAIN}/Utils"
    GATEWAYS = f"{MAIN}/Gateways"
    LOGIC = f"{MAIN}/Logic"
    PRIMITIVES = f"{MAIN}/Primitives"


class NameHelper:
    """
    A utility class to centralize the creation of node display names.
    This ensures consistent branding across all nodes in the suite.
    """

    # Define the prefix in one central place.
    PREFIX = NODES_PREFIX

    @staticmethod
    def create_display_name(name: str) -> str:
        """
        Prepends the brand prefix to a given node name.

        Args:
            name: The base name of the node (e.g., "Multiplexer").

        Returns:
            The fully formatted display name (e.g., "Ⓜ️ Multiplexer").
        """
        return f"{NameHelper.PREFIX} {name}"


class MithrilLogger:
    """
    Un logger che ispeziona lo stack di chiamate per prefissare automaticamente i messaggi
    con il DISPLAY_NAME del nodo chiamante.
    in inglese:
    A logger that inspects the call stack to automatically prefix messages
    with the DISPLAY_NAME of the calling node.
    """

    DEFAULT_PREFIX = NODES_PREFIX + "MithrilLogger"

    @staticmethod
    def log(message: str, level: str = "INFO"):
        """
        Registers a message in the console with an automatic prefix.

        Args:
            message: The message to log.
            level: The log level (e.g., INFO, WARNING, ERROR).
        """
        prefix = MithrilLogger.DEFAULT_PREFIX
        try:
            # Ispeziona lo stack di chiamate. Il frame [1] è quello del chiamante.
            caller_frame = inspect.stack()[1]
            # Ottieni l'istanza 'self' dalle variabili locali del chiamante.
            instance = caller_frame.frame.f_locals.get("self", None)

            if instance and hasattr(type(instance), "DISPLAY_NAME"):
                # Se troviamo un'istanza con un DISPLAY_NAME, lo usiamo come prefisso.
                prefix = getattr(type(instance), "DISPLAY_NAME")

        except Exception as e:
            # Se l'ispezione fallisce, non bloccare il programma, registra solo l'errore.
            print(
                f"[{MithrilLogger.DEFAULT_PREFIX}-LOG-ERROR]: Could not inspect stack: {e}"
            )

        # Stampa il messaggio di log finale e formattato.
        print(f"[{level}] [{prefix}]: {message}")


# Alias for convenience
dn = NameHelper.create_display_name
log = MithrilLogger.log
