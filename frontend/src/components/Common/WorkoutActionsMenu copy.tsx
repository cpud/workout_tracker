import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import type { WorkoutPublic } from "@/client"
import DeleteWorkout from "../Workouts/DeleteWorkout"
import EditWorkout from "../Workouts/EditWorkout"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu"

interface WorkoutActionsMenuProps {
  item: WorkoutPublic
}

export const WorkoutActionsMenu = ({ item }: WorkoutActionsMenuProps) => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <IconButton variant="ghost" color="inherit">
          <BsThreeDotsVertical />
        </IconButton>
      </MenuTrigger>
      <MenuContent>
        <EditWorkout item={item} />
        <DeleteWorkout id={item.id} />
      </MenuContent>
    </MenuRoot>
  )
}
