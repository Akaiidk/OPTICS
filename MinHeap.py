import numpy as np
from typing import List, Tuple, Dict

# On suppose que Konst est importé ou défini pour accéder à REACHABILITY_DISTANCE
# Si Konst n'est pas disponible, remplacez par l'index 6 par exemple.
try:
    from Constantes import Konst
except ImportError:
    class Konst:
        REACHABILITY_DISTANCE = 6


class HeapQueue:
    """
    Min-heap dédié à l'algorithme OPTICS avec dictionnaire de positions
    pour optimiser la mise à jour des distances d'accessibilité.
    """

    def __init__(self, Xy: np.ndarray):
        if Xy is None:
            raise ValueError("Xy n'existe pas !")
        if not isinstance(Xy, np.ndarray):
            raise TypeError("Le paramètre Xy doit être un numpy.ndarray.")

        self.heap: List[Tuple[float, int, int]] = []  # (reach_dist, counter, point_index)
        self.pos: Dict[int, int] = {}  # point_index -> position dans self.heap
        self.counter: int = 0  # Assure la stabilité (FIFO pour distances égales)
        self.Xy: np.ndarray = Xy

    # -----------------------------------------------------------------
    # Méthodes internes
    # -----------------------------------------------------------------

    def _key(self, heap_index: int) -> float:
        """Retourne la distance d'accessibilité de l'élément à la position heap_index."""
        return self.heap[heap_index][0]

    def _swap(self, i: int, j: int) -> None:
        """Échange deux éléments du tas et met à jour le dictionnaire pos."""
        # Récupération des indices des points dans Xy pour mettre à jour pos
        idx_i = self.heap[i][2]
        idx_j = self.heap[j][2]

        # Échange dans la liste
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

        # Mise à jour du dictionnaire inverse
        self.pos[idx_i], self.pos[idx_j] = j, i

    def _sift_up(self, heap_index: int) -> None:
        """Remonte l'élément à la bonne position (O(log n))."""
        parent = (heap_index - 1) // 2
        # Comparaison sur la distance (index 0), puis le counter (index 1) si égalité
        if heap_index > 0 and self.heap[heap_index] < self.heap[parent]:
            self._swap(heap_index, parent)
            self._sift_up(parent)

    def _sift_down(self, heap_index: int) -> None:
        """Descend l'élément à la bonne position (O(log n))."""
        left = 2 * heap_index + 1
        right = 2 * heap_index + 2
        smallest = heap_index

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != heap_index:
            self._swap(heap_index, smallest)
            self._sift_down(smallest)

    # -----------------------------------------------------------------
    # API publique
    # -----------------------------------------------------------------

    def push(self, point_index: int) -> None:
        """Insère un nouveau point dans le tas."""
        reach_dist = self.Xy[point_index, Konst.REACHABILITY_DISTANCE]

        # Création du tuple (distance, counter, index)
        entry = (reach_dist, self.counter, point_index)
        self.counter += 1

        # Ajout en fin de tas
        self.heap.append(entry)
        curr_pos = len(self.heap) - 1
        self.pos[point_index] = curr_pos

        # Réorganisation
        self._sift_up(curr_pos)

    def pop(self) -> Tuple[float, int]:
        """Extrait et renvoie le point de distance minimale."""
        if not self.heap:
            raise IndexError("La file est vide")

        # Sauvegarde du min (racine)
        min_entry = self.heap[0]
        reach_dist, _, min_point = min_entry

        # Suppression de l'entrée dans le dictionnaire
        del self.pos[min_point]

        if len(self.heap) > 1:
            # Le dernier élément prend la place de la racine
            last_entry = self.heap.pop()
            self.heap[0] = last_entry
            # Mise à jour de la position du point qui a bougé à la racine
            self.pos[last_entry[2]] = 0
            # On fait descendre la nouvelle racine
            self._sift_down(0)
        else:
            self.heap.pop()

        return reach_dist, min_point

    def update(self, new_reach_dist: float, point_index: int) -> None:
        """
        Met à jour la distance d'un point. 
        Si absent : insertion. Si présent et distance plus faible : update.
        """
        if point_index not in self.pos:
            # Cas 1 : Le point n'est pas dans le tas
            # On met à jour la distance dans Xy avant de push
            self.Xy[point_index, Konst.REACHABILITY_DISTANCE] = new_reach_dist
            self.push(point_index)
        else:
            # Cas 2 : Le point est déjà présent
            pos_in_heap = self.pos[point_index]
            old_reach_dist = self.heap[pos_in_heap][0]

            if new_reach_dist < old_reach_dist:
                # Mise à jour de la distance dans Xy et dans le tas
                self.Xy[point_index, Konst.REACHABILITY_DISTANCE] = new_reach_dist
                # On remplace le tuple (on garde le counter d'origine pour la stabilité)
                old_counter = self.heap[pos_in_heap][1]
                self.heap[pos_in_heap] = (new_reach_dist, old_counter, point_index)

                # Comme la distance a diminué, on ne peut que remonter
                self._sift_up(pos_in_heap)

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def __len__(self) -> int:
        return len(self.heap)

    def __repr__(self) -> str:
        return f"HeapQueue({[idx for _, _, idx in self.heap]})"

    def clear(self) -> None:
        self.heap.clear()
        self.pos.clear()
        self.counter = 0