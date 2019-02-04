class Groups:
    links = {
        "University of Michigan": "https://groupme.com/join_group/46781389/hZehS1",
    }
    def response(self, query):
        return '\n'.join(["%s -> %s" % (name, self.links[name]) for name in self.links])
