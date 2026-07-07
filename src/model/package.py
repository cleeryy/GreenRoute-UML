"""Module définissant le colis (Package) de la plateforme GreenRoute."""


class Package:
    """Représente un colis transporté par la plateforme GreenRoute.

    Attributes
    ----------
    _weight : float
        Poids du colis en kilogrammes.
    _length : float
        Longueur du colis en centimètres.
    _width : float
        Largeur du colis en centimètres.
    _height : float
        Hauteur du colis en centimètres.
    """

    def __init__(self, weight: float, length: float, width: float, height: float) -> None:
        """Initialise un nouveau colis.

        Parameters
        ----------
        weight : float
            Poids du colis en kg.
        length : float
            Longueur du colis en cm.
        width : float
            Largeur du colis en cm.
        height : float
            Hauteur du colis en cm.
        """
        self._weight = weight
        self._length = length
        self._width = width
        self._height = height

    # ── Propriétés (getters) ──────────────────────────────────────────

    @property
    def weight(self) -> float:
        """Poids du colis en kilogrammes."""
        return self._weight

    @property
    def length(self) -> float:
        """Longueur du colis en centimètres."""
        return self._length

    @property
    def width(self) -> float:
        """Largeur du colis en centimètres."""
        return self._width

    @property
    def height(self) -> float:
        """Hauteur du colis en centimètres."""
        return self._height

    # ── Propriétés calculées ──────────────────────────────────────────

    @property
    def volume(self) -> float:
        """Volume du colis en centimètres cubes (cm³)."""
        return self._length * self._width * self._height

    # ── Représentation ────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"Package(weight={self._weight}kg, "
            f"dimensions={self._length}x{self._width}x{self._height}cm)"
        )
