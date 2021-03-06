import urllib3
from .repo import Repo
import urllib3.request
import json
import datetime

# child class of Repo for github repos
class GithubRepo(Repo):
    """
    GithubRepo class.
    """
    max_elements_per_page = 100
    max_pages = 10

    def __init__(self, ctx, url):
        """
        Initialize GithubRepo class.
        """
        super().__init__(ctx, url)
                
        
    def get_owner(self):
        """
        Return owner of repo.
        """
        return self._parse_github_url(-2, "Getting owner of repo: {}")

    def get_name(self):
        """
        Return name of repo.
        """
        return self._parse_github_url(-1, "Getting name of repo: {}")

    def _parse_github_url(self, position, log_text):
        element_parsed = self.url.split('/')[position]
        self.ctx.logger.info(log_text.format(element_parsed))
        return element_parsed
        
    def _paginated_api_call(self,api_endpoint,extra_params=None):  # sourcery skip: class-extract-method
        """
        Makes a paginated call to get all the results of the call
        Docs on paginated responses here: https://docs.github.com/en/rest/guides/traversing-with-pagination
        """
        http = urllib3.PoolManager()
        headers = {'Accept': 'application/vnd.github.v3+json'}
        url = self.get_api_url(api_endpoint, extra_params)
        self.ctx.logger.info("Making first API call to {}".format(url))
        try: 
            response = http.request('GET', 
                                    url=url, 
                                    headers=headers)
        except urllib3.exceptions.MaxRetryError:
            return None
        
        data = json.loads(response.data.decode('utf-8'))
        page_number = 1
        # max number of elements per page is self.max_elements_per_page. 
        # If there are self.max_elements_per_page elements in the response, there are more pages.
        paginate = len(data) == self.max_elements_per_page
        while paginate:
            page_number += 1
            try: 
                self.ctx.logger.info("Making paginated API call to {}".format(url+"&page={}".format(page_number)))
                response = http.request('GET', 
                                        url=url + "&page={}".format(page_number), 
                                        headers=headers)
            except urllib3.exceptions.MaxRetryError:
                return data
            new_data = json.loads(response.data.decode('utf-8'))
            paginate = len(new_data) == self.max_elements_per_page and page_number < self.max_pages
            data.extend(new_data)    
        self.ctx.logger.info("Number of elements retrived: {}".format(len(data)))        
        return data

    @classmethod
    def get_api_url(self, api_endpoint, extra_params):
        url = api_endpoint+"?"
        url += "{}&".format(extra_params) if extra_params else "" 
        url += "per_page={}".format(self.max_elements_per_page)
        return url


    def get_contributors(self):  # sourcery skip: class-extract-method
        """
        Return number of contributors for repo using the 
        Github API: https://docs.github.com/en/rest/reference/repos#list-repository-contributors
        GET /repos/{owner}/{repo}/contributors
        """
        self.ctx.logger.info("Getting contributors for repo: {}".format(self.name))
        api_endpoint = "https://api.github.com/repos/{}/{}/contributors".format(self.owner, self.name)
        return (self._paginated_api_call(api_endpoint))

    def get_forks(self):
        """
        Return number of forks for repo using the 
        Github API: https://docs.github.com/en/rest/reference/repos#list-forks
        GET /repos/{owner}/{repo}/forks
        """
        self.ctx.logger.info("Getting forks for repo: {}".format(self.name))
        api_endpoint = "https://api.github.com/repos/{}/{}/forks".format(self.owner, self.name)
        return (self._paginated_api_call(api_endpoint))

    def get_releases(self):
        """
        Return number of releases for repo using the 
        Github API: https://docs.github.com/en/rest/reference/repos#list-releases
        GET /repos/{owner}/{repo}/releases
        """
        self.ctx.logger.info("Getting releases for repo: {}".format(self.name))
        api_endpoint = "https://api.github.com/repos/{}/{}/releases".format(self.owner, self.name)
        return (self._paginated_api_call(api_endpoint))

    def get_issues(self):
        """
        Return number of issues for repo using the 
        Github API: https://docs.github.com/en/rest/reference/issues#list-issues
        GET /repos/{owner}/{repo}/issues
        """
        self.ctx.logger.info("Getting issues for repo: {}".format(self.name))
        api_endpoint = "https://api.github.com/repos/{}/{}/issues".format(self.owner, self.name)
        return (self._paginated_api_call(api_endpoint, "state=all"))

    def get_commits(self):
        """
        Return number of commits for repo using the 
        Github API: https://docs.github.com/en/rest/reference/repos#list-commits
        GET /repos/{owner}/{repo}/commits
        """
        self.ctx.logger.info("Getting commits for repo: {}".format(self.name))
        api_endpoint = "https://api.github.com/repos/{}/{}/commits".format(self.owner, self.name)
        return (self._paginated_api_call(api_endpoint))

    def get_total_contributors(self):
        return len(self.contributors)

    def get_total_forks(self):
        return len(self.forks)
    
    def get_total_releases(self):
        return len(self.releases)

    def get_total_issues(self):
        return len(self.issues)

    def get_total_commits(self):
        return len(self.commits)

    def is_commit_before_date(self,commit,date):
        """
        Return True if the commit is before the date.
        """
        commit_date = datetime.datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
        return commit_date < date