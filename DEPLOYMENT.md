# GitHub Deployment Checklist

## Pre-Deployment

### Files Created ✅

- [x] `.gitignore` - Python/IDE/runtime exclusions
- [x] `LICENSE` - MIT License
- [x] `README.md` - Updated with badges and full documentation
- [x] `requirements.txt` - Python dependencies
- [x] `CONTRIBUTING.md` - Contribution guidelines
- [x] `CODE_OF_CONDUCT.md` - Community standards
- [x] `SECURITY.md` - Security policy
- [x] `.github/workflows/tests.yml` - CI/CD pipeline

### Tests Passing ✅

```
47 passed in 7.22s
```

## Deployment Steps

### 1. Initialize Git Repository

Open PowerShell in the project directory:

```powershell
cd "E:\dev\projects\The Composable Co-Developer"
git init
git add .
git commit -m "feat: initial commit - marketplace runtime complete"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `the-composable-co-developer`
3. Description: "A metacognitive co-developer marketplace runtime"
4. Visibility: Public
5. **Do NOT** initialize with README (we have one)
6. Click "Create repository"

### 3. Connect Local to GitHub

```powershell
# Add remote
git remote add origin https://github.com/ahmiershadowman-commits/the-composable-co-developer.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### 4. Verify GitHub Actions

1. Go to the repository on GitHub
2. Click "Actions" tab
3. Verify the Tests workflow is enabled
4. Wait for initial test run to complete

### 5. Add Repository Topics

On GitHub, go to Settings → Topics, add:
- `claude-code`
- `marketplace`
- `ai-assistant`
- `plugins`
- `metacognitive`
- `python`

## Post-Deployment

### Update README Badges

After first successful CI run, the test badge will show green.

### Create Release

1. Go to Releases → Create new release
2. Tag version: `v0.1.0`
3. Target: `main`
4. Title: "Initial Release - v0.1.0"
5. Description:
   ```markdown
   ## What's New
   
   - Complete marketplace runtime implementation
   - 7 macro roles (Forensics, Forge, Inquiry, Conduit, Trace, Lever, Residue)
   - 4 family executors with 18+ pipelines
   - Shared authorities and routing
   - Full test suite (47 tests)
   
   ## Installation
   
   ```bash
   claude plugin marketplace add ahmiershadowman-commits/the-composable-co-developer
   ```
   ```
6. Click "Publish release"

### Enable GitHub Pages (Optional)

For documentation site:

1. Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: /docs
4. Save

## Marketplace Distribution

### Add to Claude Code Marketplace

Create `.claude-plugin/marketplace.json` entry:

```json
{
  "name": "the-composable-co-developer",
  "source": "github:ahmiershadowman-commits/the-composable-co-developer",
  "description": "Metacognitive co-developer marketplace",
  "version": "0.1.0",
  "category": "development"
}
```

### Documentation

Ensure these are complete:
- [x] README.md (main documentation)
- [x] BUILD_CONTRACT.md (architecture spec)
- [x] CONTRIBUTING.md (how to contribute)
- [x] docs/ (detailed docs)

## Maintenance

### Regular Updates

1. Run tests before each push:
   ```bash
   python -m pytest tests -v
   ```

2. Update version in plugin.json files

3. Create git tag for releases:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

### Issue Tracking

Use GitHub Issues for:
- Bug reports
- Feature requests
- Documentation improvements

### CI/CD

GitHub Actions will automatically:
- Run tests on push
- Run tests on PR
- Report coverage

## Troubleshooting

### Git Not in Project Directory

If git commands affect wrong directory:

```powershell
# Navigate to project
cd "E:\dev\projects\The Composable Co-Developer"

# Check current git root
git rev-parse --show-toplevel

# If wrong, remove global repo and init locally
rm -Recurse -Force $env:USERPROFILE\.git
git init
```

### Permission Issues on Windows

Run PowerShell as Administrator if needed.

### Large Files

If any files are too large for GitHub:

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.pyc"
```

## Success Criteria

- [ ] Repository created on GitHub
- [ ] All files pushed successfully
- [ ] CI/CD pipeline runs green
- [ ] README displays correctly
- [ ] License visible
- [ ] Contribution guidelines accessible

---

**Last Updated**: 2026-03-25
**Version**: 0.1.0
