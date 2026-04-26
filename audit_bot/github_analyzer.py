"""
GitHub Repository Analyzer
Discovers and collects metadata from all repositories in the target account.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class RepositoryMetadata:
    """Metadata for a single repository"""
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    created_at: str
    updated_at: str
    pushed_at: Optional[str]
    size: int
    language: Optional[str]
    stargazers_count: int
    forks_count: int
    open_issues_count: int
    default_branch: str
    archived: bool
    private: bool
    
    # Computed fields
    age_days: Optional[int] = None
    is_recent: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    def compute_age(self) -> None:
        """Compute repository age in days"""
        created = datetime.fromisoformat(self.created_at.replace('Z', '+00:00'))
        now = datetime.now(created.tzinfo)
        self.age_days = (now - created).days
        self.is_recent = self.age_days < 90  # Recent if < 3 months


class GitHubAnalyzer:
    """Analyzes GitHub repositories using available tools"""
    
    def __init__(self, owner: str):
        self.owner = owner
        self.repositories: List[RepositoryMetadata] = []
        
    def parse_repository_data(self, repo_data: Dict) -> RepositoryMetadata:
        """Parse repository data from GitHub API response"""
        metadata = RepositoryMetadata(
            name=repo_data.get('name', ''),
            full_name=repo_data.get('full_name', ''),
            description=repo_data.get('description'),
            html_url=repo_data.get('html_url', ''),
            created_at=repo_data.get('created_at', ''),
            updated_at=repo_data.get('updated_at', ''),
            pushed_at=repo_data.get('pushed_at'),
            size=repo_data.get('size', 0),
            language=repo_data.get('language'),
            stargazers_count=repo_data.get('stargazers_count', 0),
            forks_count=repo_data.get('forks_count', 0),
            open_issues_count=repo_data.get('open_issues_count', 0),
            default_branch=repo_data.get('default_branch', 'main'),
            archived=repo_data.get('archived', False),
            private=repo_data.get('private', False)
        )
        metadata.compute_age()
        return metadata
    
    def load_repositories_from_file(self, filepath: str) -> None:
        """Load repository data from a JSON file (for batch processing)"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        if isinstance(data, dict) and 'items' in data:
            repos = data['items']
        elif isinstance(data, list):
            repos = data
        else:
            raise ValueError("Unexpected JSON structure")
        
        self.repositories = [self.parse_repository_data(repo) for repo in repos]
        
    def sort_by_date(self, newest_first: bool = True) -> List[RepositoryMetadata]:
        """Sort repositories by creation date"""
        return sorted(
            self.repositories,
            key=lambda x: x.created_at,
            reverse=newest_first
        )
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics"""
        if not self.repositories:
            return {}
        
        languages = {}
        for repo in self.repositories:
            if repo.language:
                languages[repo.language] = languages.get(repo.language, 0) + 1
        
        return {
            "total_count": len(self.repositories),
            "languages": languages,
            "archived_count": sum(1 for r in self.repositories if r.archived),
            "private_count": sum(1 for r in self.repositories if r.private),
            "recent_count": sum(1 for r in self.repositories if r.is_recent),
            "total_size_kb": sum(r.size for r in self.repositories),
            "total_stars": sum(r.stargazers_count for r in self.repositories),
            "avg_age_days": sum(r.age_days or 0 for r in self.repositories) / len(self.repositories)
        }
    
    def export_metadata(self, filepath: str) -> None:
        """Export metadata to JSON file"""
        data = {
            "owner": self.owner,
            "analysis_date": datetime.now().isoformat(),
            "summary": self.get_summary(),
            "repositories": [repo.to_dict() for repo in self.repositories]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
