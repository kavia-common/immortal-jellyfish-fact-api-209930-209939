from datetime import datetime, timezone
from typing import List, Tuple

from src.core.schemas import FactResponse, SourceLink
from src.util.version import get_version


class JellyfishFactService:
    """Provides curated fact data about Turritopsis dohrnii."""

    # PUBLIC_INTERFACE
    def get_fact(self) -> FactResponse:
        """Return a curated fact with supporting and refuting sources."""
        supports, refutes = self.get_sources()

        fact = (
            "Turritopsis dohrnii, often called the 'immortal jellyfish', can revert its "
            "adult medusa form back into a juvenile polyp through transdifferentiation, "
            "potentially allowing repeated life cycle resets under certain conditions."
        )
        claim = (
            "The species can avoid death from aging by reverting to an earlier life stage; "
            "however, it remains susceptible to predation, disease, and environmental threats."
        )

        return FactResponse(
            fact=fact,
            claim=claim,
            supports=supports,
            refutes=refutes,
            retrieved_at=datetime.now(timezone.utc),
            version=get_version(),
        )

    # PUBLIC_INTERFACE
    def get_sources(self) -> Tuple[List[SourceLink], List[SourceLink]]:
        """Return supporting and refuting/nuancing sources as SourceLink lists."""
        supports = [
            SourceLink(
                url="https://www.nature.com/articles/news.2010.490",
                title="Secrets of the 'immortal' jellyfish",
                stance="support",
            ),
            SourceLink(
                url="https://www.science.org/content/article/meet-immortal-jellyfish",
                title="Meet the immortal jellyfish (Science Magazine)",
                stance="support",
            ),
            SourceLink(
                url="https://www.pnas.org/doi/10.1073/pnas.0701243104",
                title="Transdifferentiation in Turritopsis (PNAS)",
                stance="support",
            ),
        ]

        refutes = [
            SourceLink(
                url="https://www.smithsonianmag.com/science-nature/there-no-such-thing-immortal-jellyfish-180974035/",
                title="There’s No Such Thing as an Immortal Jellyfish (Smithsonian)",
                stance="refute",
            ),
            SourceLink(
                url="https://www.frontiersin.org/articles/10.3389/fmars.2020.571103/full",
                title="Jellyfish blooms: ecological constraints and mortality (Frontiers in Marine Science)",
                stance="refute",
            ),
        ]

        return supports, refutes
