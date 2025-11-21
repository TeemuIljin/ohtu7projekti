class Viite:
    def __init__(self, id, tyyppi, tagit):
        self.id = id
        self.tyyppi = tyyppi
        self.tagit = tagit

    def __str__(self):
        return f"""@{self.tyyppi}{{{self.id},
{",\n".join([f"{tag} = {{{self.tagit[tag]}}}" for tag in self.tagit])}
}}"""
