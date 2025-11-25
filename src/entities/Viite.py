class Viite:
    def __init__(self, id, tyyppi, tagit):
        self.id = id
        self.tyyppi = tyyppi
        self.tagit = tagit

    def __str__(self):
        osat = ",\n".join(
            [f"{tag} = {{{self.tagit[tag]}}}" for tag in self.tagit]
        )
        return f"@{self.tyyppi}{{{self.id},\n{osat}\n}}"
