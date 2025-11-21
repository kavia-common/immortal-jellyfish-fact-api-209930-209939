from src.domain.models import FactResponse, Source


# PUBLIC_INTERFACE
def get_immortal_jellyfish_fact() -> FactResponse:
    """Return a deterministic fact about Turritopsis dohrnii with curated sources.

    No network calls are made; content is static and curated with reputable URLs.
    """
    fact_text = (
        "Turritopsis dohrnii can revert its mature medusa stage back to a juvenile polyp stage, "
        "allowing it to sidestep death under certain conditions. This phenomenon is sometimes "
        "described as 'biological immortality', but it does not prevent death from predation, "
        "disease, or unfavorable environments."
    )

    supporting = [
        Source(
            title=(
                "Reversing the life cycle: medusae reverting to polyps in Turritopsis"
            ),
            url="https://link.springer.com/article/10.1007/BF02391156",
            note="Peer-reviewed documentation of life cycle reversal (morphallaxis).",
        ),
        Source(
            title="The 'Immortal' Jellyfish That Can Transform Back Into a Polyp",
            url="https://www.nationalgeographic.com/animals/article/immortal-jellyfish",
            note=(
                "Overview of T. dohrnii's reversal ability for a general audience."
            ),
        ),
    ]

    refuting = [
        Source(
            title="No such thing as truly 'immortal' jellyfish",
            url=(
                "https://www.science.org/content/article/no-such-thing-immortal-jellyfish"
            ),
            note="Clarifies misuse of 'immortal' and real-world mortality factors.",
        ),
        Source(
            title="Immortal Jellyfish: myth and reality",
            url=(
                "https://www.nature.com/scitable/blog/science-sushi/"
                "immortal_jellyfish_immortalized_in_myth/"
            ),
            note=(
                "Contextualizes the immortality claim; death still occurs from external causes."
            ),
        ),
    ]

    return FactResponse(
        fact=fact_text,
        supporting_sources=supporting,
        refuting_sources=refuting,
    )
