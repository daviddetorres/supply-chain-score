

class Repo:
    """
    Repo class.
    """

    def __init__(self, ctx, url):
        """
        Initialize Repo class.
        """
        self.ctx = ctx
        self.url = url
        self.owner = self.get_owner()
        self.name = self.get_name()
        self.contributors = self.get_contributors()
        self.forks = self.get_forks()
        self.releases = self.get_releases()
        self.stars = self.get_stars()
        self.issues = self.get_issues()
        self.commits = self.get_commits()

    def __str__(self):
        """
        Return string representation of Repo object.
        """
        return "Repo: {0}".format(self.name)
      
    def get_contributors(self):
        """
        Return number of contributors for repo.
        """
        pass

    def get_forks(self):
        """
        Return number of forks for repo.
        """
        pass

    def get_releases(self):
        """
        Return number of releases for repo.
        """
        pass

    def get_stars(self):
        """
        Return number of stars for repo.
        """
        pass
    

    def get_issues(self):
        """
        Return number of issues for repo.
        """
        pass


    def get_commits(self):
        """
        Return number of commits for repo.
        """
        pass
    
    def get_score(self):
        """
        Return score for repo.
        """
        pass
    