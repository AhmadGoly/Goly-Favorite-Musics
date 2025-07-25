export async function handleGroupsCommand(env, userId, text) {
    const key = `${userId}_groups`;
  
    async function getGroups() {
      const data = await env.TrackifyArtist.get(key);
      return data ? JSON.parse(data) : {};
    }
    async function putGroups(groups) {
      await env.TrackifyArtist.put(key, JSON.stringify(groups));
    }
  
    const parts = text.trim().split(/\s+/);
    const cmd = parts[0].toLowerCase();
  
    if (cmd === "/makegroup") {
      if (parts.length !== 2) return "Usage: /MakeGroup groupName";
      const groupName = parts[1];
      if (groupName.includes(" ")) return "Group name cannot contain spaces.";
      const groups = await getGroups();
      if (groups[groupName]) return `Group "${groupName}" already exists.`;
      groups[groupName] = [];
      await putGroups(groups);
      return `Group "${groupName}" created.`;
    }
  
    if (cmd === "/addartist") {
      if (parts.length < 3) return "Usage: /AddArtist groupName artistName";
      const groupName = parts[1];
      const artist = parts.slice(2).join(" ").toLowerCase();
      if (groupName.includes(" ")) return "Group name cannot contain spaces.";
      const groups = await getGroups();
      if (!groups[groupName]) groups[groupName] = [];
      if (groups[groupName].includes(artist)) return `"${artist}" already in group "${groupName}".`;
      groups[groupName].push(artist);
      await putGroups(groups);
      return `Added "${artist}" to group "${groupName}".`;
    }
  
    if (cmd === "/removeartist") {
      if (parts.length < 3) return "Usage: /RemoveArtist groupName artistName";
      const groupName = parts[1];
      const artist = parts.slice(2).join(" ").toLowerCase();
      if (groupName.includes(" ")) return "Group name cannot contain spaces.";
      const groups = await getGroups();
      if (!groups[groupName]) return `Group "${groupName}" does not exist.`;
      const index = groups[groupName].indexOf(artist);
      if (index === -1) return `"${artist}" not found in group "${groupName}".`;
      groups[groupName].splice(index, 1);
      await putGroups(groups);
      return `Removed "${artist}" from group "${groupName}".`;
    }
  
    if (cmd === "/removegroup") {
      if (parts.length !== 2) return "Usage: /RemoveGroup groupName";
      const groupName = parts[1];
      if (groupName.includes(" ")) return "Group name cannot contain spaces.";
      const groups = await getGroups();
      if (!groups[groupName]) return `Group "${groupName}" does not exist.`;
      delete groups[groupName];
      await putGroups(groups);
      return `Group "${groupName}" removed.`;
    }
  
    return "Unknown command or bad usage.";
  }
  