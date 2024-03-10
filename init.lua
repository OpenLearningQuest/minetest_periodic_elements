-- Check if 'split' function does not exist and define it
if not string.split then
  function string.split(inputstr, sep)
      if sep == nil then
          sep = "%s"
      end
      local t={}
      for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
          table.insert(t, str)
      end
      return t
  end
end

-- open the elements.csv file
local elements_file = io.open(minetest.get_modpath("periodic_elements").."/elements.csv", "r")

-- Check if the file opened successfully
if not elements_file then
    minetest.log("error", "Failed to open elements.csv")
    return
end

-- Skip the header line
elements_file:read("*line")

-- create a table to store the elements
local elements = {}

-- read the file line by line
for line in elements_file:lines() do
    -- split the line by the comma
    local split = string.split(line, ",")
    -- add the element to the table
    local element_name = string.lower(split[2])
    elements[element_name] = {
        name = split[2],  -- Store the full name instead of the lowercase name for description
        symbol = split[3],
        atomic_number = split[1],
        atomic_weight = split[5],
    }
end

-- close the file
elements_file:close()

-- loop through the elements table and register nodes
for _, element in pairs(elements) do
    -- construct the texture filename by converting the symbol to lowercase
    local texture_filename = element.symbol .. ".png"

    -- register the node
    minetest.register_node("periodic_elements:" .. string.lower(element.name) .. "_block", {
        description = element.name .. " block",
        tiles = {texture_filename},
        groups = {cracky = 3, stone = 1},
    })
end