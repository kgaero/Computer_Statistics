# 📝 Documentation Update Guidelines

## Core Principle
**ALWAYS update documentation immediately after completing code changes.** These MD files are living documentation that help AI agents understand project state across coding sessions.

## Update Requirements by Change Type

### 1. Frontend Changes → docs/frontend.md
- UI/UX changes and component updates
- app architecture modifications
- New screens, widgets, or navigation changes
- State management and service integration updates
- Follow the above instruction and create or update docs/frontend.md

### 2. Backend Changes → docs/backend.md
- Google ADK agent modifications
- API endpoint changes or additions
- Authentication, CORS, or security updates
- Service integrations and deployment changes
- Follow the above instruction and create or update docs/backend.md

### 3. Testing Changes → docs/testing.md
- New test scripts or testing strategies
- Bug fixes and troubleshooting procedures
- Testing tool configurations
- QA checklist updates
- Follow the above instruction and create/update docs/testing.md

### 4. Google ADK Changes → docs/google-adk.md
Follow the instruction in the file - [instruction_for_google-adk.md](docs/instructions/instruction_for_google-adk.md)

### 5. **ALWAYS Update** → docs/main.md
- **Required for ALL changes** - describes overall repo purpose and architecture
- Project status updates (✅/🚧 indicators)
- Architecture decisions and current state
- Integration points between components

### 6. Ideas for improvement → docs/Improvement_ideas.md
Follow the instruction in the file - [instruction_for_ideas.md](docs/instructions/instruction_for_ideas.md)


## Documentation Quality Standards

### What to Include
- **Current Status**: Working vs in-progress features
- **Key Decisions**: Why something was implemented a certain way
- **Integration Points**: How components connect
- **Troubleshooting**: Common issues and solutions
- **URLs/Commands**: Production endpoints, deployment commands

### What NOT to Include
- Outdated information (remove/update immediately)
- Speculative future plans (use "Planned" sections instead)
- Code snippets without context
- Duplicate information across files

## Special Considerations
- **Cross-Session Continuity**: Other AI agents should understand project state from docs alone
- **Troubleshooting Focus**: Document solutions to problems you've solved
- **Command Preservation**: Keep working deployment/test commands up-to-date
- **Status Indicators**: Use ✅/🚧/❌ to show current state clearly

## AGENTS.md Integration

The main `/AGENTS.md` file should reference this documentation structure but NOT contain feature-
specific details. Instead, it should point AI agents to:
- Check `/docs/ai_docs/` for current work
- Use the documentation structure for understanding project features
- Follow the patterns established in completed features

This keeps AGENTS.md files stable and focused on coding patterns while feature documentation
remains dynamic.
