"""A genetic algorithm starter kit.

This module contains implementations of the basics to get started with a
specific genetic algorithm. The code here has evolved and mutated from [1].

[1] https://www.geeksforgeeks.org/genetic-algorithms/
"""

from __future__ import annotations

import random
from abc import abstractmethod
from typing import List


class Organism:

    GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP
    QRSTUVWXYZ1234567890, .-;:_!'"*#%&/()=?@${[]}'''

    def __init__(self, chromosome: str = "") -> None:
        self.chromosome = chromosome

    def __repr__(self) -> str:
        return rf"Chromosome: {self.chromosome}"

    @classmethod
    def create(cls, chromosome_length: int = None) -> Organism:
        """Create chromosome of given or random length."""
        if not chromosome_length:
            chromosome_length = random.choice(range(5, 50))
        chromosome = "".join([random.choice(cls.GENES) for _ in range(chromosome_length)])
        return cls(chromosome)

    @abstractmethod
    def reproduce(self, *args) -> Organism:
        pass


class Individual(Organism):

    prob_cutoffs = {
        "self": 0.45,
        "mate": 0.45 * 2,
    }

    def __init__(self, chromosome: str = "", *args):
        super().__init__(chromosome, *args)

    def reproduce(self, mate: Individual) -> Individual:
        """Perform reproduction and produce new offspring."""
        child_chromosome = []
        for gene_self, gene_mate in zip(self.chromosome, mate.chromosome):
            prob = random.random()
            if prob < self.prob_cutoffs["self"]:
                # get gene from self
                child_chromosome.append(gene_self)
            elif prob < self.prob_cutoffs["mate"]:
                # get gene from mate
                child_chromosome.append(gene_mate)
            else:
                # random mutation
                child_chromosome.append(random.choice(super().GENES))
        return Individual("".join(child_chromosome))


class Population:
    """Create and evolve a population towards a target chromosome."""

    def __init__(self, size: int, target_chromosome: str = "") -> None:
        self.individuals = self._create_population(size, target_chromosome)
        self._target_chromosome = target_chromosome

    @staticmethod
    def _create_population(size: int, target_chromosome: str) -> List[Individual]:
        """Create a populations of given size and chromosome length."""
        if not target_chromosome:
            target_chromosome = "".join(["_"] * random.choice(range(5, 50)))
        return [Individual.create(len(target_chromosome)) for _ in range(size)]

    def fitness_score(self, individual: Individual) -> int:
        """Fitness score for an individual w.r.t. a target."""
        score = 0
        for idx, gene in enumerate(individual.chromosome):
            if gene == self._target_chromosome[idx]:
                score += 1
        return score/len(self._target_chromosome)

    def evolve(self, verbose: bool = True) -> None:
        """Evolve towards a target chromosome."""
        if not self._target_chromosome:
            raise ValueError("Cannot evolve. Target chromosome missing.")

        cutoff_factor = 0.1
        generation_count = 1
        population = self.individuals
        target_found = False

        def print_out(generation_count: int, fittest_individual: Individual):
            """Print out during evolution."""
            if verbose:
                separator = "\n"
            else:
                separator = "\r"
            print(
                f"GENERATION: {str(generation_count).zfill(7)}"
                f"\tFITNESS SCORE: {str(round(self.fitness_score(fittest_individual), 4)).zfill(7)}"
                f"\tFITTEST INDIVIDUAL: {fittest_individual.chromosome}",
                sep=separator,
            )

        while not target_found:

            # sort population by decreasing order of fitness score
            population = sorted(
                population,
                key=lambda x: self.fitness_score(x),
                reverse=True,
            )

            # if fittest individual has fitness score of 1 we are done
            if self.fitness_score(fittest_individual := population[0]) == 1.0:
                target_found = True

            print_out(generation_count, fittest_individual)

            # generate new offsprings for new generation
            new_generation = []

            # fittest individuals go to next generation
            n_fittest_individuals = int(cutoff_factor * len(population))
            new_generation.extend(population[:n_fittest_individuals])

            # 50% of fittest Individuals will mate to produce offspring
            idx = len(population) - n_fittest_individuals
            for _ in range(idx):
                parent1 = random.choice(population[:len(population)//2])
                parent2 = random.choice(population[:len(population)//2])
                child = parent1.reproduce(parent2)
                new_generation.append(child)

            population = new_generation
            generation_count += 1

        print("\nDone.")
